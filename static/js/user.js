document.addEventListener('DOMContentLoaded', (event) => {
    const selectElement = document.getElementById('category');
    const ifFashion=document.getElementById('ifFashion');
    const HealthCare=document.getElementById('HealthCare');
    const iftoys=document.getElementById('addtoys');
    const ifdailyuse=document.getElementById('dailyuse');



    selectElement.addEventListener('change', (event) => {
        if(event.target.value=='Fashion'){
            ifFashion.style.display='flex';
            iftoys.style.display='none';
            HealthCare.style.display='none';
            ifdailyuse.style.display='none';
        }
        else if(event.target.value=='Health-Care'){
            HealthCare.style.display='flex';
            iftoys.style.display='none';
            ifFashion.style.display='none';
            ifdailyuse.style.display='none';
        }
        else if(event.target.value=='Toys'){
            iftoys.style.display='flex';
            ifFashion.style.display='none';
            HealthCare.style.display='none';
            ifdailyuse.style.display='none';
        }
        else if(event.target.value=='Daily Use'){
            ifdailyuse.style.display='flex';
            iftoys.style.display='none';
            ifFashion.style.display='none';
            HealthCare.style.display='none';
        }
        
        else{
            ifFashion.style.display='none';
            ifdailyuse.style.display='none';
            HealthCare.style.display='none';
            iftoys.style.display='none';
        }
    });
});


//  shopping page

const categ=document.getElementById('categ');
const dis=document.getElementById('dis');
const pri=document.getElementById('pri');


categ.addEventListener('change',(event)=>{
    const ifFashion=document.getElementById('fash');
    const HealthCare=document.getElementById('heal');
    const iftoys=document.getElementById('addt');
    const ifdailyuse=document.getElementById('daily');
    if(event.target.value=='Fashion'){
        ifFashion.style.display='flex';
        iftoys.style.display='none';
        HealthCare.style.display='none';
        ifdailyuse.style.display='none';
    }
    else if(event.target.value=='Health-Care'){
        HealthCare.style.display='flex';
        iftoys.style.display='none';
        ifFashion.style.display='none';
        ifdailyuse.style.display='none';
    }
    else if(event.target.value=='Toys'){
        iftoys.style.display='flex';
        ifFashion.style.display='none';
        HealthCare.style.display='none';
        ifdailyuse.style.display='none';
    }
    else if(event.target.value=='Daily Use'){
        ifdailyuse.style.display='flex';
        iftoys.style.display='none';
        ifFashion.style.display='none';
        HealthCare.style.display='none';
    }
    
    else{
        ifFashion.style.display='none';
        ifdailyuse.style.display='none';
        HealthCare.style.display='none';
        iftoys.style.display='none';
    }
});


pri.addEventListener('change',(event)=>{
    const privalue=document.getElementById('privalue');
    privalue.textContent=event.target.value;
});
dis.addEventListener('change',(event)=>{
    const disvalue=document.getElementById('disvalue');
    disvalue.textContent=event.target.value;
});


let scollelement=document.getElementById('conta');
function scrollleft() {
    scollelement.scrollLeft += 80;
}
function scrollright() {
    scollelement.scrollLeft -= 80;
}

let scollelement1=document.getElementById('conta1');
function scrollleft1() {
    scollelement1.scrollLeft += 80;
}
function scrollright1() {
    scollelement1.scrollLeft -= 80;
}

