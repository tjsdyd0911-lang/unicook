window.onload = function()
{
	$(document).on("click", "#btnLogin", function() {
		if($("#id").val() == "")
		{
			alert("아이디를 입력하세요");
			$("#id").focus();
			return;
		}	
		
		if($("#pw").val() == "")
		{
			alert("비밀번호를 입력하세요");
			$("#pw").focus();
			return;
		}
		
		$.ajax({
			url: "loginok.do",
			type: "post",
			dataType: "html",
			data :
			{
				id : $("#id").val(),
				pw : $("#pw").val()
			},
			success : function(data)
			{
				//통신이 성공적으로 이루어지면  success 가 동작함.
				data = data.trim();
				if( data == "OK" )
				{
					alert("로그인 되었습니다.");
					document.location = "";
				}else
				{
					alert("아이디 또는 비밀번호가 일치하지 않습니다.");
					$("#id").focus();
				}
			},
			error : function(xhr,status,error)
			{
				//통신 오류 발생시 error가 동작함.
				alert("실패");
			}
		});				
		
	});
}


function ShowLogin()
{
    $.ajax({
    	url : "/login.do",
    	type : "get",
    	async : true,
    	success : function(result) 
    	{
    			$("#popupModal").html(result);
    			var obj = document.getElementById("loginModal");
    			var modal = new bootstrap.Modal(obj);
    			modal.show();                 
    	},
    	error : function(request, status, error) 
    	{
    	}
    })    	
}

function ShowBunsuk(target)
{
   $.ajax({
   	url : "/bunsuk.do?target=" + target,
   	type : "get",
   	async : true,
   	success : function(result) 
   	{
   			$("#popupModal").html(result);
   			var obj = document.getElementById("analysisModal");
   			var modal = new bootstrap.Modal(obj);
   			modal.show();                 
   	},
   	error : function(request, status, error) 
   	{
   	}
   })  
}

function CartAdd(code)
{
    $.ajax({
    	url : "/cartadd.do",
    	type : "get",
    	dataType: "html",
    	data :
    	{
        	code : code,
            qty  : $(".qtyCount").text()

    	},
    	async : true,
    	success : function(data) 
    	{
				if( data == "OK" )
				{
					alert("장바구니 담기 성공!");
				}else
				{
					alert("장바구니 담기 실패!");
				}
    	},
    	error : function(request, status, error) 
    	{
        	alert("실패");
    	}
    }) 
}

function QtyMinus()
{
    
    var count = parseInt($(".qtyCount").text());
    
    if(count > 1)
    {
        count -= 1;
        $(".qtyCount").empty();
        $(".qtyCount").text(count);
    }
}

function QtyPlus()
{
    var count = parseInt($(".qtyCount").text());
    count += 1;
    $(".qtyCount").empty();
    $(".qtyCount").text(count);
}