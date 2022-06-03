# Handmade

Welcome to Handmade!

An e-commerce with a user-friendly interface
ready for all user purchases and sellings.

Project for CSE183 Web Apps

@Product
The product page displays lots of information about the product that is being viewed. Here we see a description of the product that the seller added for the customers. We also display the seller’s username and the price of the product. The username can be pressed to take the user to the seller’s profile page. Each product must contain one to four images. These are displayed in small image containers that the user can click on to focus on one image at a time. The image that is being focused is displayed in a larger image container. We used a database to store all of this information. When the page is being loaded the browser gets all of the information from the server.

If you look below you will see the rate button and the Add to Cart button. The add to cart button can be pressed when logged in to add an item to the shopping cart. When the rate button is clicked a comment section and a review section will appear below. Here users can see what others have to say about the product. Users who are logged in can leave a comment about the product. Those who are logged in and have purchased the product before can also leave a review. You will notice that reviews are written in a text area instead of a single line input area. This is because we want user reviews to be more detailed to allow customers to learn as much about a product as possible before making a purchase. The comments and reviews can be viewed by all users including those that aren’t logged in. The comments and reviews databases are both essentially the same. They contain the content, the user id of the owner, and the id of the product. This data is also grabbed from the server.

@Profile
Users also have profile pages. The profile page includes the username of the user and a catalog of items that displays the products that are being sold by that particular user. These are useful for people that want to see what a specific seller is currently selling. If you click on one of the products you will be taken to its product page. You can also click on the edit button if you are the owner of the account to edit one of your product entries. You will be able to modify any of the values and even replace the images for the product. If you are also logged in and viewing your profile you will see an add product button that can be clicked to add a product that you are trying to sell. You will also see a view orders button that will take you to a page where you can view your order history. This includes every purchase you have ever made.
