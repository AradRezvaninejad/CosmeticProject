document.addEventListener("DOMContentLoaded", function () {

const sale_price_div = document.getElementById("sale_price_div")

const currency = document.getElementById("currency")
const product_name = document.getElementById("name")
const description = document.getElementById("description")
const normal_price = document.getElementById("normal_price")
const sale_price = document.getElementById("sale_price")
const pic_file = document.getElementById("pic_file")


const save_product = document.getElementById("save_product")

const notif_div = document.getElementById("notif_div")



currency.addEventListener("change",()=>{
  console.log(currency.value)

    if (currency.value == "manual"){
        sale_price_div.style.display="none";
    }else{
        sale_price_div.style.display="inline-block";
    }
})


function shamsiToMiladi(jy, jm, jd) {
  const g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  const j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29];

  jy = parseInt(jy);
  jm = parseInt(jm);
  jd = parseInt(jd);

  let gy, gm, gd;
  let jy2 = jy - 979;
  let jm2 = jm - 1;
  let jd2 = jd - 1;

  let j_day_no = 365 * jy2 + Math.floor(jy2 / 33) * 8 + Math.floor(((jy2 % 33) + 3) / 4);
  for (let i = 0; i < jm2; ++i)
    j_day_no += j_days_in_month[i];
  j_day_no += jd2;

  let g_day_no = j_day_no + 79;

  gy = 1600 + 400 * Math.floor(g_day_no / 146097);
  g_day_no = g_day_no % 146097;

  let leap = true;
  if (g_day_no >= 36525) {
    g_day_no--;
    gy += 100 * Math.floor(g_day_no / 36524);
    g_day_no = g_day_no % 36524;

    if (g_day_no >= 365)
      g_day_no++;
    else
      leap = false;
  }

  gy += 4 * Math.floor(g_day_no / 1461);
  g_day_no %= 1461;

  if (g_day_no >= 366) {
    leap = false;
    g_day_no--;
    gy += Math.floor(g_day_no / 365);
    g_day_no = g_day_no % 365;
  }

  for (gm = 0; gm < 12; gm++) {
    let days = g_days_in_month[gm];
    if (gm == 1 && leap) days++;
    if (g_day_no < days) break;
    g_day_no -= days;
  }
  gd = g_day_no + 1;

  return `${gy}-${String(gm + 1).padStart(2, '0')}-${String(gd).padStart(2, '0')}`;
}


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
    console.log(getCSRFToken())
    const response = await fetch(`${url}`,{
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

save_product.addEventListener("click",()=>{
    if (product_name.value && description.value && normal_price.value && pic_file.value){
            const file = pic_file.files[0];
  
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                  let src = e.target.result
                  
                console.log("nufvhdf")
                let miladi =""
                if (currency.value=="timing" && sale_price.value){
                  const [jy, jm, jd] = sale_price.value.split('/');
                  miladi = shamsiToMiladi(jy, jm, jd);
                }
                
                  post_("http://127.0.0.1:8000/api/Blog/",{"work":"add_blog","content":description.value,"slug":normal_price.value,"title":product_name.value,"timeing":currency.value=="timing" ? miladi : null,"image":src,"is_published":false,"is_timing":currency.value},"POST").then(result=>{
                    console.log(result)
                    console.log("regreg")
                    if (result.ok){
                        notif_div.innerHTML = `	<div class="alert alert-success alert-dismissible fade show" role="alert">
                        <strong>Holy guacamole!</strong>${result.matn}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                      </div>`;
                    }
                    else{
                        notif_div.innerHTML = `	<div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <strong>Holy guacamole!</strong>${Object.values(result.matn)[0][0
                          
                        ]}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                      </div>`
                    }
                })
                    
                }
                reader.readAsDataURL(file);
            }

        }else{
            notif_div.innerHTML = `	<div class="alert alert-warning alert-dismissible fade show" role="alert">
            <strong>Holy guacamole!</strong>لطفا تمامی فیلد ها را پر کنید
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`
        }
    
    })
  });