# Eater API
Eater Whatsapp API Documentation

**HOST** `http://api.blablabla.us`

### Example API Entry
**Title**	**Create Client**
**URL**	`/client`
**Method**	**GET**
**URL Parameters**	**Required:**
`None`
**Success Response**	**Code:** 200
**Content:**`API is running..!!!`
**Error Response**	**Code:** 401 UNAUTHORIZED
**Content:**`{"error": "Log in"}`
**Error Response**	**Code:** 422 UNPROCESSABLE ENTRY
**Content:**`{"error": "Email Invalid"}`
**Sample Request**	`/scenario?id=55`
**Notes**	
```js
$.ajax({
  url: "/scenario?id=55",
  dataType: "json",
  type: "GET",
  success: function(r) {
    console.log(r);
}});
```
