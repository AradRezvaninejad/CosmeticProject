const sale_price_div = document.getElementById("sale_price_div")

const currency = document.getElementById("currency")
const product_name = document.getElementById("name")
const description = document.getElementById("description")
const normal_price = document.getElementById("normal_price")
const sale_price = document.getElementById("sale_price")
const pic_file = document.getElementById("pic_file")
const category = document.getElementById("category")
const sub_category = document.getElementById("sub-category")
const quantity = document.getElementById("quantity")

const pic_file_div = document.getElementById("pic_file_div")
const pic_file2 = document.getElementById("pic_file2")
const pic_file3 = document.getElementById("pic_file3")
const pic_file4 = document.getElementById("pic_file4")
const pic_file5 = document.getElementById("pic_file5")

const save_product = document.getElementById("save_product")

const notif_div = document.getElementById("notif_div")


pic_file.addEventListener("chnage",()=>{
    pic_file_div.classList.remove("none")
})


currency.addEventListener("change",()=>{
    if (currency.value == "normal_price"){
        sale_price_div.style.display="none";
    }else{
        sale_price_div.style.display="inline-block";
    }
})

if (product_name.value && description.value && normal_price.value && sale_price.value && pic_file.value && category.value && sub_category.value && quantity.value)

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
  headers:{"Content-Type":'application/json',
  "X-Requested-With":"XMLHttpRequest",
  "X-CSRFToken":getCSRFToken()

},
body:JSON.stringify(data)
})
const resp =await response.json()

return resp
}
console.log("salam")
post_("http://127.0.0.1:8000/dashboard-admin/add-product",{"work":"get_categoriz"}).then(result=>{
    console.log(result)
    if (!result.sub_category || !result.category){
        notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
        <strong>Holy guacamole!</strong>قبل از اضافه کردن کالا باید نوع و کتگوری اضافه کنید
      </div>`
    }
})

save_product.addEventListener("click",async ()=>{
  console.log(  product_name.value + description.value + normal_price.value + pic_file.value + category.value + sub_category.value + quantity.value)
    if (product_name.value && description.value && normal_price.value && pic_file.value && category.value && sub_category.value && quantity.value){
        if(/^\d+$/.test(quantity.value) && /^\d+$/.test(normal_price.value)){
            const natijeTasvir = await main(); 
            console.log(natijeTasvir)
            if (!natijeTasvir){
                alert("kewfo")
            }

                  post_("http://127.0.0.1:8000/dashboard-admin/add-product",{"work":"add_product","description":description.value,"normal_price":normal_price.value,"name":product_name.value,"sub_category":sub_category.value,"sale_price":sale_price.value,"picture":natijeTasvir,"category":category.value,"quantity":quantity.value,"is_sale":currency.value}).then(result=>{
                    if (result.ok){
                        notif_div.innerHTML = `	<div class="alert alert-success alert-dismissible fade show" role="alert">
                        <strong>Holy guacamole!</strong>${result.matn}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                      </div>`
                    }
                    else{
                        notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <strong>Holy guacamole!</strong>${result.matn}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                      </div>`
                    }
                })
                    


            }else{
                notif_div.innerHTML = `	<div class="alert alert-warning alert-dismissible fade show" role="alert">
                <strong>Holy guacamole!</strong>لطفا فیلد های اعداد را عدد وارد کنید
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>`;
}

          console.log("121212")
        }else{
            notif_div.innerHTML = `	<div class="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>Holy guacamole!</strong>لطفا تمامی فیلد ها را پر کنید
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`
        }
    
    })



    
async function readAsBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

async function sendToRemoveBg(base64) {
    const formData = new FormData();
    formData.append("size", "auto");
    formData.append("image_file", base64);
  
  const response = await fetch('https://api.remove.bg/v1.0/removebg', {
    method: 'POST',
    headers: {
      'X-Api-Key': '6xjuct7Yw1tg1DNj27yLqTi4',
    },
    body: formData
  });

  if (!response.ok) {
    alert("خطا در ارتباط با remove.bg. لطفاً بررسی کن.");
    throw new Error("Remove.bg error: " + response.status);
  }

  return await response.blob();
}

async function drawOnWhiteCanvas(blob) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = function () {
      const canvasWidth = 500;
      const canvasHeight = 650;

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = canvasWidth;
      canvas.height = canvasHeight;

      ctx.fillStyle = "rgb(248, 248, 248)";
      ctx.fillRect(0, 0, canvasWidth, canvasHeight);

      const x = (canvasWidth - img.width) / 2;
      const y = (canvasHeight - img.height) / 2;
      ctx.drawImage(img, x, y);

      const finalImage = canvas.toDataURL('image/png');
      resolve(finalImage);
    };

    img.src = URL.createObjectURL(blob);
  });
}

async function main() {
    const file = pic_file.files[0];
    console.log("nduif")
    if (!file) {
      alert("لطفاً یک فایل انتخاب کنید.");
      return null;
    }
  
    try {
      const base64 = await readAsBase64(file);
      const bgRemovedBlob = await sendToRemoveBg(file);
      const natijeTasvir = await drawOnWhiteCanvas(bgRemovedBlob);
      
  
      return natijeTasvir;
  
    } catch (err) {
      console.error("خطا:", err);
      alert("مشکلی پیش اومد. جزئیات در کنسول.");
      return null;
    }
  }
  