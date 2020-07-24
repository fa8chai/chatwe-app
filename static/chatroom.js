document.addEventListener('DOMContentLoaded',()=>{
    
    $('html, body').animate({ scrollTop: $('#end').offset().top }, 'slow');

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // 
        document.querySelector('.btn8').onclick=function(){
            console.log('btn8')
            message = document.querySelector('.message').value;
            document.querySelector('.message').value='';
            channel = document.querySelector('.namech').innerHTML;
            socket.emit('add message',{'message':message,'channel':channel})

        }


        document.querySelector('.join').onclick= function(){
            console.log('hiiii')
            channel=document.querySelector('.namech').innerHTML;
            socket.emit('join',{'channel':channel,'username':document.querySelector("#username").innerHTML});
            
            
       }
       document.querySelector('.leave').onclick=function(){
        console.log('hihihi')
        channel=document.querySelector('.namech').innerHTML;
        socket.emit('leave',{'channel':channel,'username':document.querySelector("#username").innerHTML});
     
   
           }
   

        
    });

    socket.on('broadcast message',data =>{
       var header = document.createElement('h6');
       var p = document.createElement('p');
       var small =document.createElement('small');
       var div = document.createElement('div');
       

       header.innerHTML=data['username'];
       p.innerHTML = data['message'];
       small.innerHTML=data['dt_string'];
       

       div.append(header);
       div.append(p);
       div.append(small);

       if (data['username'] == document.querySelector('#username').innerHTML){
        div.classList.add('chatm', 'me');
        document.querySelector('#messageList').append(div);
       }
       else{
       div.classList.add('chatm');
       document.querySelector('#messageList').append(div);

       }
       $('html, body').animate({ scrollTop: $('#end').offset().top }, 'slow');

    })

    socket.on('status',data => {
  
       var div = document.createElement('div');
       div.classList.add("alert","alert-info","alert-dismissible","fade","show");
       div.innerHTML= data['msg']
       div.style.width="100%";
       div.style.height="auto";
       div.style.margin="0px";
       div.style.padding="7px";
       div.style.fontWeight="bold";
       div.style.textAlign="center";
       document.querySelector('.list2').append(div);
      
       
        document.querySelector('.join').style.display="none";
        document.querySelector('.leave').style.display="block"



       setTimeout(function() {
        $(".alert").alert('close');
    }, 4000);
   

})



    


})