const publish_unpublish = document.querySelectorAll("#publish_unpublish")
const detail_blog = document.querySelectorAll("#detail_blog")
const edit_blog = document.querySelectorAll("#edit_blog")
const delete_blog = document.querySelectorAll("#delete_blog")
const blogz = document.querySelectorAll("#blogz")
const filter_blogz = document.getElementById("filter_blogz")
const search_title = document.getElementById("search_title")


async function post_(url,data,methodd){
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
    console.log("hduivhsodhivwefwefewfewfwefwefwegergwethgwthwhtrh")
    const response = await fetch(`${url}/`,{
  method:methodd,
  headers:{"Content-Type":'application/json',
    "X-CSRFToken":getCSRFToken()
},
credentials: 'include',
body:JSON.stringify(data)
})
const resp =await response.json()

return resp
}


publish_unpublish.forEach(every=>{
    every.addEventListener("click",()=>{

    post_(`http://127.0.0.1:8000/api/Blog/${every.dataset.slug}`,{"is_published":every.dataset.publish =="unPublish" ? false : true},"PATCH").then(result=>{
        if(result.ok){
            Swal.fire({
                title: `${every.dataset.publish =="unPublish" ? "unPublished" : "Published"}`,
                text: result.matn || '',
                icon: 'success',
                confirmButtonText: 'تأیید'
              }).then(() => {
                location.reload()
              })
        }
    })

    })
})


delete_blog.forEach(every=>{
    every.addEventListener("click",()=>{
        
    post_(`http://127.0.0.1:8000/api/Blog/${every.dataset.slug}`,{},"DELETE").then(result=>{
        if(result.ok){
            Swal.fire({
                title: `hazf shod`,
                text: result.matn || '',
                icon: 'success',
                confirmButtonText: 'تأیید'
              }).then(() => {
                location.reload()
              })
        }
    })

    })

})

console.log(blogz)

filter_blogz.addEventListener("change",()=>{
    if(filter_blogz.value == "show_all"){
        blogz.forEach(every=>{
            every.classList.remove("none")
        })
    }else{
        blogz.forEach(every=>{
            if (filter_blogz.value == every.dataset.state){
                every.classList.remove("none")
            }else{
                every.classList.add("none")
            }
        })
    }

})

search_title.addEventListener("input",()=>{
    if (search_title.value){
        console.log("wvugwviuwehweiv")

        const value = search_title.value.toLowerCase().trim();

        blogz.forEach((item) => {
            const state = item.dataset.title.toLowerCase();
    
            if (state.startsWith(value) || value === "") {
                item.classList.remove("none2");
            } else {
                item.classList.add("none2");
            }
        });


    }else{
    console.log("00000000000000000000000000")

        blogz.forEach(every=>{
            every.classList.remove("none2")
        })
    }
})