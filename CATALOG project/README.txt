Instructions
run database_setup.py
run autofill.py (This will populate the databse with some random data)
run application.py(This will start the web application)

Interface manual:
 goto localhost:8000/ or localhost:8000/catalog (This will take you to the first page and list all categories)
 There will be a login button for user to login with out doing this the CUD operations shown below would not be available . Without logging in only read option is available
 <option when logged in>
 You should see an add option this is to add categories , you should also see delete option by the side of each category clicking it will delete the category

 clicking on any of the category will take you to a page that contains list of items within the category here you can perform CURD operations by clicking respective links.


Note:- This project is submitted under IOT foundations , problem is CSS and other webstyling is not covered . 
since i am not from a CS background i have created only a minimalisitc app with text , I would have researched 
it and added the features its due to deadline i am submitting  this code.In case if its compulsory i shall try to add CSS elements. 

Json links :

http://localhost:8000/catalog/JSON - node for displaying catagories in catalog

http://localhost:8000/catalog/<category name>/list/JSON - node for displaying items in a category , replace the category space with necessary category name.

Thank You