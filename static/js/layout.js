 // toggle menu
 let toggle = document.querySelector('.toggle');
 let navigation = document.querySelector('.navigation');
 let main = document.querySelector('.main');

 toggle.onclick = function(){
     navigation.classList.toggle('actived');
     main.classList.toggle('actived');
 }

 // active Link
 let list = document.querySelectorAll('.navigation li');

 function activeLink(){
     list.forEach((item) => 
     item.classList.remove('actived'));
     this.classList.add('actived');
 }
 list.forEach((item) =>
     item.addEventListener('click', activeLink))
