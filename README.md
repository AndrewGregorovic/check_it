# Check It :white_check_mark:

This app aims to help users manage checklists of tasks to avoid the hassle of having to remember everything in our busy lives. The app will allow you to:
- [x] Create new lists with an accompanying title, description (optional) and thumbnail image (optional)
- [x] Edit current lists, including the ability to:
    - [x] Check items off after you complete them
    - [x] Reset lists to uncheck all list items
    - [x] Add list items
    - [x] Delete list items
    - [x] Rearrange list items
- [x] Delete lists

You will also be able to mark lists to be repeated daily or weekly which will automatically reset the list accordingly.

Using the app requires an account which allows your list data to be synchronised between multiple devices so that you can use the app on your phone or computer and pick up right where you left off.

---

## Table of Contents
- [Installation](#installation)
- [Implementation Plan](#implementation-plan)
- [CI/CD](#ci-cd)
- [Wireframes](#wireframes)

## Installation

1. Clone the repository, `git clone https://github.com/AndrewGregorovic/check_it.git`
2. Navigate to the app directory, `cd <path/to/directory>/check_it`
3. Install a virtual environment, `python3 -m venv venv`
    > Install the venv module if you are missing it, `pip3 install venv`
4. Activate the environment, `source venv/bin/activate`
5. Install dependencies, `pip install -r requirements.txt`
6. Run the app, `python src/main.py`

## Implementation Plan

The development of this project is being tracked with the Github Projects section of this repository. The link is included below for easy navigation to the project board,

[https://github.com/AndrewGregorovic/check_it/projects/1](https://github.com/AndrewGregorovic/check_it/projects/1)

## CI/CD

The CI/CD workflow for this project makes use of github actions to perform the set up for jobs and runs on the latest stable version of Ubuntu.

> Currently only the continuous integration part of the workflow is implemented as the project is in it's initial stages.

The workflow is initiated when commits are pushed to the master branch, it uses Python 3.9.0 to run the automated unit tests and code checks to determine if the code is in working order.

## Wireframes

#### Landing Page
Initial page that is seen when visited by users who either don't have an account or aren't logged in yet. Gives a little discription of the app and a screenshot of it to the side, along with buttons/links to log in or sign up.

The app name at the top left should link back to this page if there is no logged in user, otherwise it should link to the user's dashboard page.

![Landing Page Wireframe](docs/wireframes/landing_page.png)

#### Log In/Sign Up Page
Basic log in or sign up page, the background could be another screenshot of the app or some other stylish designs so that it isn't a plain white background.

![Log In/Sign Up Page Wireframe](docs/wireframes/login_signup_page.png)

#### Dashboard Page
The dashboard is seen when the "Today's lists" option is selected (it is selected by default and it should be highlighted or something to indicate when selected). The arrows are used when there's multiple lists in each category for the user to navigate between while staying on the dashboard. The circles by each checklist name are optional thumbnail images that can be uploaded for each list.

The circle by the user name in the top right is the user's profile picture, the picture + user name when clicked will show a dropdown with options to view profile details or log out.

If lists have more items than can be viewed on the screen, make the list scrollable within it's section. When the list title or thumbnail image is clicked it opens the view list page for that list. When a list item is clicked it toggles the checkbox for that item.

![Dashboard Page Wireframe](docs/wireframes/dashboard_page.png)

#### User Profile Page
Displays the different pieces of profile information. The user name, name and email fields are just text when viewing the profile but when edit profile is clicked the fields become editable. The change password section and button to change profile picture is only visible when edit profile is clicked. While editing profile information the edit profile button becomes a save profile button. The back button returns the user to their dashboard page.

![User Profile Page Wireframe](docs/wireframes/user_profile_page.png)

#### Saved Lists Page
This is seen when the "All lists" option is selected (it should be highlighted or something to indicate that). There is another set of options that show to allow the user to filter their lists (again needs some sort of indication of being selected). Having a large number of lists will grow the list down and create a vertical scrollbar.

The whole tile for each list will link to the view list page for that list. The top right of each tile indicates if the list repeats daily, weekly or not at all, if not at all there is no daily/weekly label.

![Saved Lists Page Wireframe](docs/wireframes/saved_lists_page.png)

#### Create List Page
This card can be created on top of the page currently being viewed or can be a separate page with something in the background. When create list is clicked it takes the user to the edit list page for the newly created list.

![Create List Page Wireframe](docs/wireframes/create_list_page.png)

#### Edit List Page
To implement the ability to rearrange list items, either allow each item to be dragged up and down with the mouse or need to add in up/down buttons that appear for the item currently moused over which can move the item in the appropriate direction.

![Edit List Page Wireframe](docs/wireframes/edit_list_page.png)

#### View List Page
This page is viewed when a list is clicked on. Clicking list items on this page will toggle their checkbox, this is the only page other than the dashboard where list items can be toggled between checked and not checked. The reset button at the top right of the list view can be clicked to reset the completion state of all the lists items, i.e. it marks everything as not completed. Clicking back takes the user back to their dashboard page.

![View List Page Wireframe](docs/wireframes/view_list_page.png)