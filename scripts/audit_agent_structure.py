import os

def main():
    required_dirs = [
        ".agent/skills",
        ".agent/knowledge",
        ".agent/methodology",
        ".agent/debug",
        ".agent/sources",
        ".github/workflows",
        "scripts",
        "docs",
        "examples"
    ]
    
    missing = []
    for d in required_dirs:
        if not os.path.isdir(d):
            missing.append(d)
    
    if missing:
        print(f"❌ Missing directories: {missing}")
        exit(1)
    
    print("✅ Structure seems correct")

if __name__ == "__main__":
    main()
