const category_name = document.getElementById("product_name")
const category_slug = document.getElementById("product_slug")
const description = document.getElementById("description")
const create_category = document.getElementById("create_category")
const notif_div = document.getElementById("notif_div")



async function post_(url,data){
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(cookie => {
                let trimmedCookie = cookie.trim();
                if (trimmedCookie.startsWith('csrftoken=')) {
                    cookieValue = trimmedCookie.split('=')[1];
                }
            });
        }
        return cookieValue;
    }
    const response = await fetch(`${url}`,{
  method:"POST",
  headers:{"Content-Type":'aplication/json',
  "X-Requested-With":"XMLHttpRequest",
  "X-CSRFToken":getCSRFToken()

},
body:JSON.stringify(data)
})
const resp =await response.json()

return resp
}

create_category.addEventListener("click",()=>{
    if (category_name.value && category_slug.value && description.value){
        console.log("sssssssssss")
        post_("http://127.0.0.1:8000/dashboard-admin/sub_categories",{"work":"add_cat","description":description.value,"slug":category_slug.value,"name":category_name.value}).then(result=>{
            if (result.ok){
                notif_div.innerHTML = `	<div class="alert alert-success alert-dismissible fade show" role="alert">
                <strong>Holy guacamole!</strong> You should check in on some of those fields below.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>`
            }
            else{
                notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong>Holy guacamole!</strong> You should check in on some of those fields below.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>`
            }
        })
    }else{
        notif_div.innerHTML = `	<div class="alert alert-warning alert-dismissible fade show" role="alert">
		<strong>Holy guacamole!</strong> You should check in on some of those fields below.
		<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
	  </div>`
    }
})
