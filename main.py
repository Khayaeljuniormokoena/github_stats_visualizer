from visualizer import Visualizer

def main():
    owner = input("Enter owner of GitHub repository: ")
    repo = input("Enter name of GitHub repository: ")

    vis = Visualizer(owner, repo)
    
    print("1. Lines Over Time")
    print("2. Commits By Author")
    print("3. Stargazer History")
    print("4. Commit Activity")
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        vis.lines_over_time()
    elif choice == "2":
        vis.commits_by_author()
    elif choice == "3":
        vis.stargazer_history()
    elif choice == "4":
        vis.commit_activity()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
