const banner_title = document.getElementById("banner_title")
const big_content = document.getElementById("big_content")
const small_content = document.getElementById("small_content")
const button_text = document.getElementById("button_text")
const currency_label = document.getElementById("currency_label")

const url = document.getElementById("url")

const c_brands = document.getElementById("c_brands")
const c_categorys = document.getElementById("c_categorys")
const c_products = document.getElementById("c_products")


const currency = document.getElementById("currency")
const pic_file = document.getElementById("pic_file")
const save_banner = document.getElementById("save_product")

const image = document.getElementById("image")
const notif_div = document.getElementById("notif_div")

let brands_ok=true
let categorys_ok=true
let products_ok = true
let image_ok = ""
let orgin_src = image.src
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
    console.log("sending data:", data)
    console.log("json:", JSON.stringify(data))
    const response = await fetch(`${url}`,{
  method:"POST",
  headers: {"Content-Type": "application/json",
  "X-Requested-With":"XMLHttpRequest",
  "X-CSRFToken":getCSRFToken()

},
body:JSON.stringify(data)
})
const resp =await response.json()

return resp
}



post_("http://127.0.0.1:8000/dashboard-admin/add_banner/",{'work':"get_brands&categoris&products"}).then(result=>{
    console.log(result)
    brands_ok = result.brands
    categorys_ok = result.categoriz
    products_ok = result.products
})
console.log(brands_ok)
pic_file.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const img = new Image();
    const objectURL = URL.createObjectURL(file);
    img.src = objectURL;

    img.onload = function () {
        const width = img.width;
        const height = img.height;
        const ratio = width / height;

        if (ratio < 1.3 || ratio > 2.0) {
            image_ok="لطفاً تصویری مستطیلی انتخاب کن (مثلاً نسبت 16:9 یا 3:2)"
            notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Holy guacamole!</strong>${image_ok}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`;
          image.src =orgin_src
            return;
        }

        if (width < 1000 || height < 500) {
            image_ok="کیفیت تصویر پایینه. لطفاً تصویری با کیفیت بالاتر انتخاب کن"
            notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Holy guacamole!</strong>${image_ok}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`;
          image.src =orgin_src
            return;
        }
        image_ok="y"
        image.src=img.src
        notif_div.innerHTML = ``;
    };

    img.onerror = function () {
        alert("فایل تصویر معتبر نیست");
        image_ok="فایل تصویر معتبر نیست"
    };
});


currency.addEventListener("change",()=>{
    if (currency.value =="url"){
        currency_label.innerHTML="custom url"
        currency_label.classList.remove("reddd")
        url.classList.remove("none")
        c_brands.classList.add("none")
        c_categorys.classList.add("none")
        c_products.classList.add("none")
    }
    else if(currency.value =="brands"){
        if(!brands_ok){
            currency_label.classList.add("reddd")
            currency_label.innerHTML ="no brand detected"
        }else{
            currency_label.innerHTML ="brands"
            currency_label.classList.remove("reddd")
        }
        url.classList.add("none")
        c_brands.classList.remove("none")
        c_categorys.classList.add("none")
        c_products.classList.add("none")

    }
    else if(currency.value =="categorys"){
        if(!categorys_ok){
            currency_label.classList.add("reddd")
            currency_label.innerHTML ="no category detected"
        }else{
            currency_label.innerHTML ="categorys"
            currency_label.classList.remove("reddd")
        }
        
        url.classList.add("none")
        c_brands.classList.add("none")
        c_categorys.classList.remove("none")
        c_products.classList.add("none")
    }
    else if(currency.value =="products"){
        if(!products_ok){
            currency_label.classList.add("reddd")
            currency_label.innerHTML ="no product detected"
        }else{
            currency_label.innerHTML ="products"
            currency_label.classList.remove("reddd")
        }
        url.classList.add("none")
        c_brands.classList.add("none")
        c_categorys.classList.add("none")
        c_products.classList.remove("none")
    }
})

save_banner.addEventListener("click",()=>{

    if (banner_title.value && big_content.value && small_content.value && button_text.value && pic_file.value){
        if (image_ok=="y"){
            let related_value = ""
            if (currency.value =="categorys"){

                related_value = c_categorys.value

            }else if(currency.value =="products"){

                related_value = c_products.value

            }else if(currency.value =="brands"){

                related_value = c_brands.value
                
            }else if(currency.value =="url"){
                
                related_value = url.value
                
            }
            console.log(related_value)
            if (related_value){
                const file = pic_file.files[0];
                console.log('fetching')
        
                if (file) {
                    
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                      let src = e.target.result
                    
                console.log('fetching')
                post_("http://127.0.0.1:8000/dashboard-admin/add_banner/",{"work":"add_banner","banner_title":banner_title.value,'big_content':big_content.value,"small_content":small_content.value,"button_text":button_text.value,"picture":src,"related":currency.value,"related_value":related_value}).then(result=>{console.log(result);

                    if(result.ok){
                    notif_div.innerHTML = `	<div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Holy guacamole!</strong>${result.matn}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>`;
                    }else{
                        notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <strong>Holy guacamole!</strong>${result.matn}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                      </div>`;
                    }

                })
                }
                reader.readAsDataURL(file);}
            }else{
                notif_div.innerHTML = `	<div class="alert alert-warning alert-dismissible fade show" role="alert">
                <strong>Holy guacamole!</strong>لطفا تمامی فیلد ها را پر کنید
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>`;
            }


        }else{
            notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Holy guacamole!</strong>${image_ok}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`;
        }
    }else{
        notif_div.innerHTML = `	<div class="alert alert-warning alert-dismissible fade show" role="alert">
		<strong>Holy guacamole!</strong>لطفا تمامی فیلد ها را پر کنید
		<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
	  </div>`;
    }

})
