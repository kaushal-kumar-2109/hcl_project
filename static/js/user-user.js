const profileinfo=document.getElementById('profileinfo');
const addressinfo=document.getElementById('addressinfo');
const profileform=document.getElementById('profiledata');
const addressform=document.getElementById('addressdata');

profileinfo.addEventListener('click',()=>{
    profileform.style.display='flex';
    addressform.style.display='none'
});
addressinfo.addEventListener('click',()=>{
    addressform.style.display='flex';
    profileform.style.display='none';
});

const personalinfo=document.getElementById("personalinfo");
const personalinfoform=document.getElementById('personalinfoform');

personalinfo.addEventListener("click",()=>{
    personalinfoform.innerHTML=`
    <fieldset>
                    <input name="username" id="username" type="text" placeholder="User Name" style="color: gray;">
                    
                    <div class="gender">
                    <label for="male" style="color: gray;">Male</label>
                    <input type="radio" name="gender" id="male" value="M">

                    <label for="female" style="color: gray;">female</label>
                    <input type="radio" name="gender" id="female" value="F">

                    <label for="other" style="color: gray;">Other</label>
                    <input type="radio" name="gender" id="other" value="O">
                    </div>
                    <button>Save</button>&nbsp;&nbsp;
                </fieldset>
    `;
});

document.getElementById('emailinfo').addEventListener("click",()=>{
    document.getElementById('emaiform').innerHTML=`
    <fieldset>
                    <input name="email" id="email" type="email" placeholder="abc@gmail.com" style="color: gray;">
                    <button>Save</button>
                </fieldset>
    `;
});

document.getElementById('phonenumberdata').addEventListener("click",()=>{
    document.getElementById('phonenumberform').innerHTML=`
    <fieldset>
                    <input name="number" id="number" type="text" value="+91" style="color: gray;">
                    <button>Save</button>
                </fieldset>
    `;
});
