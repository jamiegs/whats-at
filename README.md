# whats-at
Monitors  restaurant/brewery websites, keeps a easily searchable list and notifies people of favorites

test 123

## Includes 
- Web Scrapper to read which burgers are at different abes locations.

- Static Webpages for people to see current burgers

- Notifies people via email/text of their favorites.

- Lambda function to remove email/text also.

# Data Format

Resturant items
- Item, Description, Date Added
Locations
- Name, Address 
LocationBurgers
- Name, ItemName, DateSet
Favorites
- email/phone, Item, Location

Returns 
	Burger Name, Ingredients, Location

	Store in database

	Store list of burgers in database
	Trigger notification when new burger is added

	Allow people to get text/email when burger shows up

	People can saw which burger and choose locations
	OR
	Send email/text weekly with updated burgers for their locations.

# Could also be used for beer


Data Access Patterns

GetAllActiveItems,SortedByLocation
GetAllItemsByLocation,Sorted ByItemName.
GetAllUniqueItems
GetAllNotificationsByItem
GetAllNotificationsByNotificationAddress

