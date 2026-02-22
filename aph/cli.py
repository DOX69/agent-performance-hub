"""APH CLI — Main entry point for the Agent Performance Hub CLI.

Commands:
    aph init                — Initialize .agent/ with core skills
    aph list                — List all available skills
    aph list --installed    — Show installed skills only
    aph search <query>      — Search skills by keyword
    aph add <skill> [...]   — Install one or more skills
    aph remove <skill>      — Remove a skill
    aph update              — Update all installed skills
    aph update <skill>      — Update a specific skill
    aph info <skill>        — Show detailed info about a skill
    aph version             — Show CLI version
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .config import CORE_SKILLS
from .installer import (
    init_project,
    install_skill,
    is_initialized,
    get_installed_skills,
    remove_skill,
    update_all_skills,
    update_skill,
)
from .registry import (
    get_all_categories,
    get_all_skills,
    get_skill_by_name,
    get_skills_by_category,
    search_skills,
)

console = Console()


@click.group(context_settings={"help_option_names": ["-h", "--help"], "max_content_width": 120})
def main():
    """🚀 APH — Agent Performance Hub

    PURPOSE:
    Manage AI agent skills across your projects.
    Install curated skills for Gemini, Claude, and other AI agents.
    
    USAGE:
    aph [COMMAND] [ARGS]...
    
    COMMANDS:
    init                Initialize .agent/ with core skills
    list                List available skills (remote or installed)
    search              Search skills by name, specific tags, or description
    add                 Install one or more skills
    remove              Remove a skill
    update              Update installed skills
    info                Show detailed info about a skill
    version             Show APH version
    
    EXIT_CODES:
    0 = Success
    1 = Error (e.g., project not initialized, skill not found)
    
    EXAMPLES:
    aph init
    aph list --category devops
    aph add docker-expert
    """
    pass


# ─── aph version ──────────────────────────────────────────────────────────────

@main.command()
def version():
    """Show APH version.

    PURPOSE:
    Display the currently installed version of APH CLI.

    USAGE:
    aph version

    OUTPUT:
    Text: aph v<version>

    EXIT_CODES:
    0 = Success
    """
    console.print(f"[bold cyan]aph[/] v{__version__}")


# ─── aph init ─────────────────────────────────────────────────────────────────

@main.command()
@click.option(
    "--skills",
    default=None,
    help="Comma-separated list of skills to install (default: core skills).",
)
def init(skills):
    """Initialize .agent/ with core skills in the current project.

    PURPOSE:
    Scaffolds the .agent directory structure and installs default core skills.
    Must be run once per project before using other commands.

    USAGE:
    aph init [OPTIONS]

    OPTIONS:
    --skills <list>     Comma-separated list of skills to install instead of defaults.

    OUTPUT:
    Status messages indicating created directories and installed skills.

    EXIT_CODES:
    0 = Success
    1 = Error (Project already initialized or installation failed)

    PRECONDITIONS:
    Current directory must not already contain a valid .agent configuration.

    EXAMPLES:
    aph init
    aph init --skills brainstorming,docker-expert
    """
    console.print()
    console.print(
        Panel(
            "[bold cyan]APH — Agent Performance Hub[/]\n"
            "Initializing your project with AI agent skills...",
            border_style="cyan",
        )
    )

    skills_list = None
    if skills:
        skills_list = [s.strip() for s in skills.split(",")]
        console.print(f"\n📦 Custom skills: [yellow]{', '.join(skills_list)}[/]")
    else:
        console.print(f"\n📦 Core skills: [yellow]{', '.join(CORE_SKILLS)}[/]")

    success, message = init_project(skills=skills_list)

    if success:
        console.print(f"\n{message}")
    else:
        console.print(f"\n[red]{message}[/]")
        raise SystemExit(1)


# ─── aph list ─────────────────────────────────────────────────────────────────

@main.command(name="list")
@click.option("--installed", is_flag=True, help="Show only installed skills.")
@click.option("--category", default=None, help="Filter by category.")
def list_skills(installed, category):
    """List available skills.

    PURPOSE:
    Browse the skills registry or view installed skills.

    USAGE:
    aph list [OPTIONS]

    OPTIONS:
    --installed     Show ONLY skills currently installed in this project.
    --category <name>   Filter skills by category (e.g., 'devops', 'frontend').

    OUTPUT:
    Table with columns: Status (✅/empty), Skill Name, Category, Description.

    EXIT_CODES:
    0 = Success
    1 = Error (Project not initialized when using --installed)

    EXAMPLES:
    aph list
    aph list --installed
    aph list --category security
    """
    if installed:
        if not is_initialized():
            console.print("[red]Project not initialized. Run 'aph init' first.[/]")
            raise SystemExit(1)
        installed_names = get_installed_skills()
        skills = [
            s for s in get_all_skills() if s["name"] in installed_names
        ]
        title = f"Installed Skills ({len(skills)})"
    elif category:
        skills = get_skills_by_category(category)
        title = f"Skills — Category: {category} ({len(skills)})"
    else:
        skills = get_all_skills()
        title = f"All Available Skills ({len(skills)})"

    if not skills:
        console.print("[yellow]No skills found.[/]")
        return

    # Show installed status
    installed_set = set(get_installed_skills()) if is_initialized() else set()

    table = Table(title=title, show_lines=False, border_style="cyan")
    table.add_column("Status", width=3, justify="center")
    table.add_column("Skill", style="bold", min_width=25)
    table.add_column("Category", style="dim", min_width=12)
    table.add_column("Description", max_width=60)

    for skill in sorted(skills, key=lambda s: s["name"]):
        status = "✅" if skill["name"] in installed_set else "  "
        core_badge = " ⭐" if skill.get("core") else ""
        desc = skill.get("description", "")
        # Truncate long descriptions
        if len(desc) > 60:
            desc = desc[:57] + "..."
        table.add_row(
            status,
            skill["name"] + core_badge,
            skill.get("category", "—"),
            desc,
        )

    console.print()
    console.print(table)
    console.print()

    # Show categories summary
    if not installed and not category:
        categories = get_all_categories()
        console.print(
            f"[dim]Categories: {', '.join(categories)}[/]\n"
            "[dim]Filter: aph list --category <name>[/]\n"
            "[dim]⭐ = core skill (installed with aph init)[/]"
        )


# ─── aph search ───────────────────────────────────────────────────────────────

@main.command()
@click.argument("query")
def search(query):
    """Search skills by name, description, or tags.

    PURPOSE:
    Find skills matching a keyword.

    USAGE:
    aph search <query>

    ARGUMENTS:
    query   Search term (case-insensitive).

    OUTPUT:
    Table of matching skills.

    EXIT_CODES:
    0 = Success (even if no matches found)

    EXAMPLES:
    aph search docker
    aph search "react patterns"
    """
    results = search_skills(query)

    if not results:
        console.print(f"[yellow]No skills matching '{query}'.[/]")
        console.print("[dim]Try a broader term or run 'aph list' to see all.[/]")
        return

    installed_set = set(get_installed_skills()) if is_initialized() else set()

    table = Table(
        title=f"Search Results for '{query}' ({len(results)} found)",
        border_style="cyan",
    )
    table.add_column("Status", width=3, justify="center")
    table.add_column("Skill", style="bold", min_width=25)
    table.add_column("Category", style="dim")
    table.add_column("Description", max_width=60)

    for skill in results:
        status = "✅" if skill["name"] in installed_set else "  "
        desc = skill.get("description", "")
        if len(desc) > 60:
            desc = desc[:57] + "..."
        table.add_row(
            status,
            skill["name"],
            skill.get("category", "—"),
            desc,
        )

    console.print()
    console.print(table)


# ─── aph add ──────────────────────────────────────────────────────────────────

@main.command()
@click.argument("skills", nargs=-1, required=True)
@click.option("--category", default=None, help="Install all skills in a category.")
def add(skills, category):
    """Install one or more skills.

    PURPOSE:
    Add new skills to the current project.

    USAGE:
    aph add [OPTIONS] [SKILLS]...

    ARGUMENTS:
    skills  One or more skill names to install.

    OPTIONS:
    --category <name>   Install ALL skills from this category (overrides skill list).

    OUTPUT:
    Success/failure status for each installed skill.

    EXIT_CODES:
    0 = Success
    1 = Error (Project not initialized or no skills found in category)

    PRECONDITIONS:
    Project must be initialized with 'aph init'.

    EXAMPLES:
    aph add docker-expert
    aph add docker-expert nestjs-expert
    aph add --category frontend
    """
    if not is_initialized():
        console.print("[red]Project not initialized. Run 'aph init' first.[/]")
        raise SystemExit(1)

    # If --category flag, override skill list
    if category:
        cat_skills = get_skills_by_category(category)
        if not cat_skills:
            console.print(f"[yellow]No skills found in category '{category}'.[/]")
            return
        skills = [s["name"] for s in cat_skills]
        console.print(
            f"📦 Installing {len(skills)} skill(s) from category [cyan]{category}[/]..."
        )

    installed_count = 0
    for skill_name in skills:
        success, msg = install_skill(skill_name)
        if success:
            console.print(f"  ✅ {msg}")
            installed_count += 1
        else:
            console.print(f"  [red]❌ {msg}[/]")

    console.print(f"\n[green]Done! {installed_count}/{len(skills)} skill(s) installed.[/]")


# ─── aph remove ───────────────────────────────────────────────────────────────

@main.command()
@click.argument("skill_name")
@click.option("--force", is_flag=True, help="Skip confirmation.")
def remove(skill_name, force):
    """Remove a skill from the project.

    PURPOSE:
    Delete an installed skill from .agent/skills/.

    USAGE:
    aph remove [OPTIONS] <skill_name>

    ARGUMENTS:
    skill_name  Name of the skill to remove.

    OPTIONS:
    --force     Skip confirmation prompt.

    OUTPUT:
    Success/failure message.

    EXIT_CODES:
    0 = Success
    1 = Error (Project not initialized or skill not installed)

    EXAMPLES:
    aph remove docker-expert
    aph remove --force docker-expert
    """
    if not is_initialized():
        console.print("[red]Project not initialized.[/]")
        raise SystemExit(1)

    if not force:
        if not click.confirm(f"Remove skill '{skill_name}'?"):
            console.print("[dim]Cancelled.[/]")
            return

    success, msg = remove_skill(skill_name)
    if success:
        console.print(f"✅ {msg}")
    else:
        console.print(f"[red]❌ {msg}[/]")


# ─── aph uninstall ────────────────────────────────────────────────────────────

@main.command()
@click.option("--force", is_flag=True, help="Skip confirmation.")
def uninstall(force):
    """Uninstall APH from the system and remove .agent/ directory.

    PURPOSE:
    Completely remove the Agent Performance Hub from your project and system.
    WARNING: This action is destructive and cannot be undone.

    USAGE:
    aph uninstall [OPTIONS]

    OPTIONS:
    --force     Skip confirmation prompt.

    OUTPUT:
    Success/failure message.

    EXIT_CODES:
    0 = Success
    1 = Error

    EXAMPLES:
    aph uninstall
    aph uninstall --force
    """
    from .installer import uninstall_aph as installer_uninstall_aph

    if not force:
        click.secho(
            "WARNING: This will remove the .agent/ directory and uninstall the 'aph' package.",
            fg="red", bold=True
        )
        if not click.confirm("Are you sure you want to proceed?"):
            console.print("[dim]Cancelled.[/]")
            return

    success, msg = installer_uninstall_aph()
    if success:
        console.print(f"✅ {msg}")
    else:
        console.print(f"[red]❌ {msg}[/]")
        raise SystemExit(1)


# ─── aph update ───────────────────────────────────────────────────────────────

@main.command()
@click.argument("skill_name", required=False, default=None)
def update(skill_name):
    """Update installed skills to the latest version.

    PURPOSE:
    Update one or all skills from the registry.

    USAGE:
    aph update [SKILL_NAME]

    ARGUMENTS:
    skill_name  (Optional) Specific skill to update. If omitted, updates ALL.

    OUTPUT:
    Status for each updated skill.

    EXIT_CODES:
    0 = Success
    1 = Error (Project not initialized or skill not installed)

    EXAMPLES:
    aph update                (Updates all skills)
    aph update docker-expert  (Updates only docker-expert)
    """
    if not is_initialized():
        console.print("[red]Project not initialized. Run 'aph init' first.[/]")
        raise SystemExit(1)

    if skill_name:
        success, msg = update_skill(skill_name)
        if success:
            console.print(f"✅ Updated '{skill_name}'")
        else:
            console.print(f"[red]❌ {msg}[/]")
    else:
        console.print("🔄 Updating all installed skills...")
        updated, errors, error_msgs = update_all_skills()
        console.print(f"\n✅ Updated {updated} skill(s).")
        if errors:
            console.print(f"[yellow]⚠ {errors} skill(s) had issues:[/]")
            for err in error_msgs:
                console.print(err)


# ─── aph info ─────────────────────────────────────────────────────────────────

@main.command()
@click.argument("skill_name")
def info(skill_name):
    """Show detailed information about a skill.

    PURPOSE:
    View metadata, description, and installation status of a skill.

    USAGE:
    aph info <skill_name>

    ARGUMENTS:
    skill_name  Name of the skill to view.

    OUTPUT:
    Panel with Name, Category, Tags, Core status, Size, and Description.

    EXIT_CODES:
    0 = Success
    1 = Error (Skill not found)

    EXAMPLES:
    aph info docker-expert
    """
    skill = get_skill_by_name(skill_name)

    if not skill:
        console.print(f"[red]Skill '{skill_name}' not found.[/]")
        console.print("[dim]Run 'aph list' to see available skills.[/]")
        raise SystemExit(1)

    installed_set = set(get_installed_skills()) if is_initialized() else set()
    is_inst = skill_name in installed_set

    panel_text = Text()
    panel_text.append(f"Name:        ", style="dim")
    panel_text.append(f"{skill['name']}\n", style="bold")
    panel_text.append(f"Category:    ", style="dim")
    panel_text.append(f"{skill.get('category', '—')}\n")
    panel_text.append(f"Tags:        ", style="dim")
    panel_text.append(f"{', '.join(skill.get('tags', []))}\n")
    panel_text.append(f"Core:        ", style="dim")
    panel_text.append(f"{'Yes ⭐' if skill.get('core') else 'No'}\n")
    panel_text.append(f"Installed:   ", style="dim")
    panel_text.append(
        "Yes ✅\n" if is_inst else "No\n",
        style="green" if is_inst else "red",
    )
    panel_text.append(f"Size:        ", style="dim")
    panel_text.append(f"{skill.get('size_kb', '?')} KB\n")
    panel_text.append(f"\n")
    panel_text.append(f"Description:\n", style="dim")
    panel_text.append(f"{skill.get('description', 'No description available.')}")

    console.print()
    console.print(Panel(panel_text, title=f"📦 {skill_name}", border_style="cyan"))

    if not is_inst:
        console.print(f"\n[dim]Install with: aph add {skill_name}[/]")


if __name__ == "__main__":
    main()

