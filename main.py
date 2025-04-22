from bs4 import BeautifulSoup
import csv
import requests
import sys

CSET_STAFF_URL = 'https://cset.georgetown.edu/team'

def fetch_html(url):
    """Make an GET request and return HTML string or None

    Args:
        url (str): The URL to make the request to

    Returns:
        str (optional): The HTML of the fetched URL, if any
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch: {response.status_code}")
        return None

def get_staff_urls():
    """Fetch a list of profile URLs for the staff members at CSET

    Returns:
        list[str]: A list of URLs, each corresponding to a profile page for a CSET staff member
    """
    response = fetch_html(CSET_STAFF_URL)
    soup = BeautifulSoup(response, "html.parser")
    return [a['href'] for a in soup.find_all("a", class_="staff__link", href=True)]

def scan_staff_page(url):
    """Scrapes a staff page and returns relevant data in a dictionary

    Args:
        url (str): The URL of a CSET staff member's profile page

    Returns:
        dict: The fetched data from the page (name, title, teams, photo_link, biography)
    """
    response = fetch_html(url)
    soup = BeautifulSoup(response, "html.parser")

    data = {}

    staff_title = soup.find(class_="staff-title")
    if staff_title:
        # Extract name, title, team(s)
        title_content = staff_title.find(class_="staff-title__content")
        if title_content:
            name = title_content.find("h1")
            if name:
                data["name"] = name.text.strip()
            title = title_content.find("span")
            if title:
                data["title"] = title.text.strip()
            # There can be more than 1 team a person is on
            teams = title_content.find_all("h6")
            data["teams"] = [team.text.strip().strip(',') for team in teams]

        # Extract photo link
        photo = staff_title.find(class_="staff-title__photo")
        if photo:
            img = photo.find("img")
            if img:
                data["photo_link"] = img.get('src')

    # Extract biography
    bio = soup.find(class_="post-content")
    if bio:
        data["biography"] = bio.text.strip()

    # If we can't even get the name, return None
    if data.get('name'):
        return data
    else:
        return None

def write_staff_data_to_csv(staff_dict, filename):
    """Write staff data from dictionary to CSV

    Args:
        staff_dict (dict): Dictionary mapping staff names to corresponding data
        filename (str): The filename to write the data to.
    """
    fieldnames = ['Name', 'Title', 'Team(s)', 'Biography', "Photo Link"]

    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for staff_member in staff_dict.values():
            writer.writerow(
                {
                    'Name': staff_member.get('name'),
                    'Title': staff_member.get('title'),
                    'Team(s)': "; ".join(staff_member.get('teams')).strip(),
                    'Biography': staff_member.get('biography'),
                    'Photo Link': staff_member.get('photo_link'),
                }
            )

    print("Successfully wrote to CSV")

def main(required_teams, output_filename):
    # Get URLs for all staff members
    staff_urls = get_staff_urls()
    # Go to each staff member's profile and scrape data
    staff_dict = {}
    print(f"Scraping {len(staff_urls)} staff profiles...")
    for i, url in enumerate(staff_urls):
        print(f"Processing {i+1}/{len(staff_urls)}: {url}")
        staff_info = scan_staff_page(url)
        if staff_info:
            # Skip staff member if they aren't on a team we're querying for
            if required_teams:
                if not any(team in staff_info.get("teams", []) for team in required_teams):
                    continue
            name = staff_info['name']
            staff_dict[name] = staff_info
        else:
            print(f"Unable to scrape data at URL {url}")
    # Write to CSV
    write_staff_data_to_csv(staff_dict, output_filename)

if __name__ == "__main__":
    required_teams = []
    output_filename = 'CSET_Staff.csv'
    # Read from command line arguments
    if "--teams" in sys.argv:
        idx = sys.argv.index("--teams")
        try:
            teams = sys.argv[idx + 1]
            required_teams = [team.strip() for team in teams.split(',')]
        except IndexError:
            print("Error: --teams flag requires a comma-separated argument")
            sys.exit(1)
    if "--output-filename" in sys.argv:
        idx = sys.argv.index("--output-filename")
        try:
            output_filename = sys.argv[idx + 1]
            if not output_filename.endswith('.csv'):
                print("Error: Output filename must end in .csv")
                sys.exit(1)
        except IndexError:
            print("Error: --output-filename flag requires a filename argument")
            sys.exit(1)
    # Run the script
    main(required_teams, output_filename)
