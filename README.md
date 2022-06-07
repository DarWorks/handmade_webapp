# Handmade

Welcome to Handmade!

An e-commerce with a user-friendly interface
ready for all user purchases and sellings.

Project for CSE183 Web Apps

## Developers: Darien Cruz Nguyen | Jonathan Muniz-Murguia | Aaron Chen | Yashaswi Bathula | Amaan Sheikh


### Homepage

The homepage or the index page is where a user would ideally land while searching for the site.
The purpose of this page is to create an impression for both existing and new users.
The left-hand side of the page contains a store navigation section which helps users redirect to a product category page based on the text (product category) they click.
The particular product category they click will lead to the page displaying products for the category.
Additionally, in the same section when a user is logged in, a button redirecting to the logged in users profile and a button redirecting to a page where the user can add a product to be sold.
The main body of the page displays 2 product rows each displaying 4 products.
The second row of the section will always contain randomised products from the database. 
The point of displaying randomised products is to give users an overview of some other products that are available on the site.
The type of information displayed on the first row is dependent on whether a user is logged in or not. 
When a user is logged in, the products that match the users preferences will be displayed on the first row. When a user is not logged in, the products that have been recently added to the database will be displayed. 

The homepage has product focused cards which display the most appropriate or most relevant information that would be matter to a user exploring the products on the site. The cards contain information like product name, product seller name, the current rating of the product, price. An image of the product is also displayed and when any user clicks on the image, they will be redirected to the products page. The view button on the bottom of the cards also has the same functionality. Similarly, when a user clicks on the sellers name, they will be redirected to the seller profiles page. Additionally, the rating displayed on the cards is based on the aggregate rating from all the users who rated the product.
 

### Product Categories

The products from a particular product category are displayed here. 
The user is directed to this page from the homepage depending on the category they click.
This page does not have a limit to displaying products, it will display all products which belong to the product category clicked.
Lastly, the cards structure is same as that of the homepage.




### Personalization 

The personalization page is the interface that allows new users to select a unique username and set shopping preferences that will allow a tailored experience within the website. Upon sign-in, a non-personalized user is presented with a pop-up notification in the bottom, right-hand corner of their screen. This notification greets the user using the first name that was chosen upon signing up for the website, along with a button labeled ‘Personalize!’ that, once clicked, will direct them to the personalization page. 

The primary notification prompt is conditionally rendered to a user's screen given that the ‘isPersonalized’ attribute of an authenticated user is set to 'False'. Hovering over the notification initializes the 'hover' attribute, where the initial 60% opacity rendering of the notification is transitioned to 100% opacity. Once the ‘Personalize!’ button is clicked, the user is immediately taken to a new window where they can input their personalization information.

The upper portion of the personalization page prompts the user to select a username. Here, the user can choose any username that is unique and non-empty. This cross-check validation is done by comparing the user's choice to the store's existing database, as well as by monitoring the contents of the entry box to ensure it is non-empty. Given that a username fails to meet the criteria of uniqueness or being non-empty, an error message is prompted upon submission and appears below the entry box to explain the specific issue. 
The lower portion of the page, labeled “Top Three Product Preferences”, allows the user to choose three shop categories from those offered in the store. There are three drop-down entry boxes that each offer choice categories, “ Jewelry and Accessories”, “Clothing and Shoes”, “Home and Living”, “Toys and Entertainment”, and “Art and Collectibles”, and “Other”. 

Once a user is satisfied with their choices, they are left to click the “Submit!” button, located at the bottom of the entry boxes. This button starts the cross-checking validation of the user’s entries and can result in two outcomes. One outcome is the successful acceptance of the user’s choice of username, which simply inserts the data into the store’s database and also redirects the user back to the home screen. The second outcome is the display of an error message prompting the user to choose a different username, this occurs given that the user’s initial choice fails the above-mentioned constraints. At this point, the user will be able to select another available username and, upon success, will be redirected to the home page. 
The completion of the personalization feature sees that a user’s top three preferences and their username are inserted into the user profile database, this allows the rest of the site to tailor portions of the experience for the specific logged-in user (i.e the ‘for-you’ portion of the home page). Additionally, the ‘isPersonalized’ attribute of a user in the store database is set to ‘True’ upon successful customization, this characteristic allows further permissions on the website, such as selling items. 

The personalization page can be arrived at in several other ways, given that a user needs to provide additional information to the site. These features, such as the 'Profile' page and the 'Sell and Item' page will redirect the user to the 'Personalization' page, given that the authenticated user attempting to use these features is non-personalized. 

### Layout

The layout was implemented in layout.html and implements a navbar that includes a home button linked to the page logo and a buy button that has a dropdown menu including all the types of items to be sold on our website. The navbar in the layout also includes a sign in and sign up button that allows the user to register with our website to access our features. It lastly includes a search bar that searches for any current items in our website. Lastly the layout includes a breadcrumbs footer that leads to the about us page and faq page that gives information on the team and the website. The css used for the layout is within the Bulma library. The about page and faq page are implemented using variables to track the state of which the element in question, the answer for example, should be shown or not. 

### Product

The product page displays lots of information about the product that is being viewed. Here we see a description of the product that the seller added for the customers. We also display the seller’s username and the price of the product. The username can be pressed to take the user to the seller’s profile page. Each product must contain one to four images. These are displayed in small image containers that the user can click on to focus on one image at a time. The image that is being focused is displayed in a larger image container. We used a database to store all of this information. When the page is being loaded the browser gets all of the information from the server.

If you look below you will see the rate button and the Add to Cart button. The add to cart button can be pressed when logged in to add an item to the shopping cart. When the rate button is clicked a comment section and a review section will appear below. Here users can see what others have to say about the product. Users who are logged in can leave a comment about the product. Those who are logged in and have purchased the product before can also leave a review. You will notice that reviews are written in a text area instead of a single line input area. This is because we want user reviews to be more detailed to allow customers to learn as much about a product as possible before making a purchase. The comments and reviews can be viewed by all users including those that aren’t logged in. The comments and reviews databases are both essentially the same. They contain the content, the user id of the owner, and the id of the product. This data is also grabbed from the server.

### Rating and Notification

The website also has a rating system for every product. The rating system is only for personalized users and every user is able to add a rating to any product and it will be added to the overall rating in which each product has. Any non-personalized or non-logged in user will be redirected to either the personalization or login pages. The ratings are based on a star system, assigning a rating between 0 and 5 stars. By clicking the amount of stars the user would like to rate the product, the user submits the rating to the overall rating. To change the rating simply moving your cursor to another star and clicking will edit the rating value and resubmit it to the overall rating. This was implemented in the product.html page and product.js script. This was done using a new database and adding a total rating number and a total rating count to count both the number of stars given and the number of raters for the product. The new database holds the information of all ratings. Our website also has the ability to notify a user to log in if they are not yet logged in. If a user is not logged in then code can be deployed to have a notification appear instead of the profile button to remind the user to log in if they have an account. 

### Profile

Users also have profile pages. The profile page includes the username of the user and a catalog of items that displays the products that are being sold by that particular user. These are useful for people that want to see what a specific seller is currently selling. If you click on one of the products you will be taken to its product page. You can also click on the edit button if you are the owner of the account to edit one of your product entries. You will be able to modify any of the values and even replace the images for the product. If you are also logged in and viewing your profile you will see an add product button that can be clicked to add a product that you are trying to sell. You will also see a view orders button that will take you to a page where you can view your order history. This includes every purchase you have ever made.

### Selling a Product

A signed user can sell a crafted or unique item from the Profile page or the Home page by listing it for sale on the Handmade Platform.  With this page, the user can input information relating to the item they want to put up for sale.  Input such as Product name, type, description, quantity, price, and images are collected.  The user can choose up to four files to use in their product listing.  Each of these input tags is important and plays a crucial role in the website functionality; therefore, if a user does not provide a piece of information for any of these fields, the page prompts them to do so before allowing them to submit.  Once submitted, the user is free to return to their profile page.  

### Messaging (not in production) (see branch messaginglinking) 

Our website also has a system that allows for users to connect with a seller that does contract art in which the seller and all buyers can communicate with each other to buy custom art. This is a feature that a seller can gain during personalization and the messaging system that connects the buyers to the seller is employed on the sellers profile page. The messaging system has all buyers and the seller connected to one message board.

### Shopping Cart

The shopping is the last stop before the destination.  The customer can access this page anytime by clicking the shopping cart icon on any page when browsing Handmade.  From here, the customer will be displayed with rows of the products they have added to their card.  If there are no items in the cart, a friendly reminder to add items to the cart will be provided.

When the customer has selected an array of items, they will be listed with a picture preview of the item, the product name, price, and quantity.  The customer can increase the number of items in the cart to the amount available in stock.  If the customer no longer is interested in a particular item, they can press the red “X” to clear the item from their cart.  All items are stored in Local Storage, and all users will have access to their own personal cart.  Upon completing the order, the items will be removed from the shopping cart.

Lastly, when the customer is ready to purchase their items, they can look on the right to view the checkout box.  Here a subtotal counter that changes as the customer updates and deletes the products will be displayed.  As well, information relating to the shipping name and address will be requested.  When ready, the customer will press the checkout button, and the payment will securely be handled by stripe.  Once the customer successfully purchases the goods, they will be presented with a success page thanking them for their order.  Upon unsuccessful purchase, the user is instead re-routed to the homepage where they can continue shopping where they last left.

### View Orders

The user who wants to look at all their orders placed can access this information inside their profile page or after purchasing a product from Handmade Crafts.  The information provided is a simple grid filled with information regarding the purchase.  In addition, details such as user email, order date, ordered items, fulfillment, paid dates, and more are included on this page.
