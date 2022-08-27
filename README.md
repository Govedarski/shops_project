# REST API Shops application - SoftUni exam project

# About project

Flask REST API. The project is only for educational purposes.
There is 4 groups of users: customers, shop owners, admins and super admins:

<div>Customers can:</div>
<ul>
    <li>register</li>
    <li>create and modify delivery address details</li>
    <li>buy products</li>
</ul>

<div>Shop owners:</div>
<ul>
    <li>register</li>
    <li>create and modify shops</li>
    <li>create and modify products</li>
</ul>

<div>Admins can:</div>
<ul>
<li>modify site content</li>
</ul>

<div>Super admins can::</div>
<ul><li>modify site content</li>
<li>create admins</li></ul>

## Install

    pip install -r requirements.txt

## Run the app

    For Unix, Linux, macOS, etc.:
        $ export FLASK_APP=hello
        $ flask run
    
    For Windows:
        > set FLASK_APP=hello
        > flask run

## Third party services

* AWS S3 - service which stores the uploaded files that are uploaded by users
* Stripe - payment provider which generate payment links for online payment

## API Endpoints summary

<div><a href="#register">Register</a></div>
<div><a href="#login">Login</a></div>
<div></div><a href="#cd">Customer details</a></div>
<div></div><a href="#sod">Shop owner details</a></div>
<div></div><a href="#dad">Delivery address details</a></div>
<div><a href="#shops_endpoints">Shops</a></div>
<div><a href="#products">Products</a></div>

<div id ="register"></div>

## Register Endpoints

<details>
<summary> 
    Register user
</summary>

    Url: /users/register
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Register admin
</summary>

    Url: /users/register
    Methid: Post
    request: TODO
    Response: TODO
    Description: TODO

</details>

<div id ="login"></div>

## Login Endpoints

<details>
<summary> 
    Login
</summary>

    Url: /login
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>

<div id ="cd"></div>

## Customer Details Endpoints

<details>
<summary> 
    Create
</summary>

    Url: /customer_details
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Get single
</summary>

    Url: /customer_details/<pk>
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Edit
</summary>

    Url: /customer_details/<pk>
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Delete profile picture
</summary>

    Url: /customer_details/<pk>/profile_picture
    Methid: DELETE
    request: TODO
    Response: TODO
    Description: TODO

</details>


<div id ="sod"></div>

## Shop Owner Details Endpoints

<details>
<summary> 
    Create
</summary>

    Url: /shop_owner_details
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Get single
</summary>

    Url: /shop_owner_details/<pk>
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Edit
</summary>

    Url: /shop_owner_details/<pk>
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Delete profile picture
</summary>

    Url: /shop_owner_details/<pk>/profile_picture
    Methid: DELETE
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Verify 
</summary>

    Url: /shop_owner_details/<pk>/verify
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<div id ="dad"></div>

## Delivery Address Details Endpoints

<details>
<summary> 
    Create
</summary>

    Url: /delivery_address_details
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Get single
</summary>

    Url: /delivery_address_details/<pk>
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Get list
</summary>

    Url: /delivery_address_details
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>


<details>
<summary> 
    Edit
</summary>

    Url: /delivery_address_details/<pk>
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Delete
</summary>

    Url: /delivery_address_details/<pk>
    Methid: Delete
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Verify 
</summary>

    Url: /shop_owner_details/<pk>/verify
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<div id ="#shops_endpoints"></div>

## Shops Endpoints

<details>
<summary> 
    Create
</summary>

    Url: /shops
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Get single
</summary>

    Url: /shops/<pk>
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Get list
</summary>

    Url: /shops
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>




<details>
<summary> 
    Edit
</summary>

    Url: /shops/<pk>
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Delete brand logo
</summary>

    Url: /shops/<pk>/brand_logo
    Methid: delete
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Verify 
</summary>

    Url: /shops/<pk>/verify
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Deactivate
</summary>

    Url: /shops/<pk>/deactivate
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<div id ="products"></div>

## Products Endpoints

<details>
<summary> 
    Create
</summary>

    Url: /product
    Methid: POST
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Get single
</summary>

    Url: /product/<pk>
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Get list
</summary>

    Url: /product/<pk>
    Methid: GET
    request: TODO
    Response: TODO
    Description: TODO

</details>




<details>
<summary> 
    Edit
</summary>

    Url: /product/<pk>
    Methid: PUT
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Delete
</summary>

    Url: /product/<pk>
    Methid: DELETE
    request: TODO
    Response: TODO
    Description: TODO

</details>

<details>
<summary> 
    Delete photo
</summary>

    Url: /product/<pk>/product_photo
    Methid: delete
    request: TODO
    Response: TODO
    Description: TODO

</details>

## Author Name

Velislav Govedarski

## License

This project is licensed with the [MIT license](LICENSE).
