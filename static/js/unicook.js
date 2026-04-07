// ajax 통신으로 로그인 처리
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

// 로그인 페이지 모달 ajax로 활성화
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
// 장바구니에 상품 추가
function CartAdd(code)
{
    $.ajax({
    	url : "/cartadd.do",
    	type : "get",
    	dataType: "json",
    	data :
    	{
        	code : code,
            qty  : $(".qtyCount").text()

    	},
    	async : true,
    	success : function(response) 
    	{
        	if(response.result === "success") {
                alert("장바구니 담기 성공!");
             
                $("#cart-badge").text(response.new_count);
                
            } else {
                alert(response.message || "장바구니 담기 실패!");
            }
    	},
    	error : function(request, status, error) 
    	{
        	alert("실패");
    	}
    }) 
}
// 수량 감소
function QtyMinus(obj)
{
    var qtyCount = $(obj).siblings(".qtyCount")
    var count    = parseInt(qtyCount.text());
    
    if(count > 1)
    {
        count -= 1;
        qtyCount.text(count);
    }
}
// 수량 증가
function QtyPlus(obj)
{
    var qtyCount = $(obj).siblings(".qtyCount")
    var count    = parseInt(qtyCount.text());
    count += 1;
    qtyCount.text(count);
}

// 장바구니 체크박스 및 선택삭제 부분
$(document).ready(function()
{
    // 전체선택 및 해제
    $("#selectAll").on("change", function() {
        $(".item-checkbox").prop("checked", $(this).is(":checked"));
    });
    
    // 개별 체크박스 변경 시 전체선택 체크박스 상태 업데이트
    $(document).on("change", ".item-checkbox", function() {
        const total = $(".item-checkbox").length;
        const checked = $(".item-checkbox:checked").length;
        
        $("#selectAll").prop("checked", total === checked);
    });
    
    // 선택 삭제 버튼 클릭 시
    $("#btnDeleteSelected").on("click", function() {
        const checkedItems = $(".item-checkbox:checked");
        
        if (checkedItems.length === 0) {
            alert("삭제할 상품을 선택해주세요.");
            return;
        }

        if (confirm("선택한 상품을 장바구니에서 삭제하시겠습니까?")) {
            const cnoList = [];
            checkedItems.each(function() {
                // 체크된 항목의 부모 컨테이너에서 cno 값을 가져옴
                cnoList.push($(this).closest(".cart-item-container").data("cno"));
            });
            // 선택한 상품 삭제 및 DB 최신화 함수 호출
            deleteCartItems(cnoList);
        }
    });
    
});
// 선택한 상품 삭제 및 DB 최신화
function deleteCartItems(cnos)
{
    $.ajax({
        url: "/cartdelete.do", // 실제 서버 측 삭제 처리 URL
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({ "cnos": cnos }),
        success: function(response) {
            console.log("서버 응답:", response);
            if (response.result === "success" || response.status === "ok") {
                // 서버 삭제 성공 시 UI에서 해당 항목들 제거
                cnos.forEach(function(cno) {
                    $(".cart-item-container[data-cno='" + cno + "']").remove();
                    $("#cart-badge").text(response.new_count);
                    updateFinalTotal();
                    if (response.new_count == 0) {
                        $("#cart-badge").empty();
                    }
                    
                    // 삭제 후 전체선택 상태 다시 계산
                    const total = $(".item-checkbox").length;
                    const checked = $(".item-checkbox:checked").length;
                    $("#selectAll").prop("checked", total > 0 && total === checked);
                });
            } else {
                alert("삭제 중 오류가 발생했습니다.");
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
            alert("서버와 통신할 수 없습니다.");
        }
    });
}

// 선택삭제 버튼 클릭 시
function deleteSelectItems()
{
    var cnos = [];
    // 체크박스들 중 체크된 것만 골라서 cno를 수집
    $(".item-checkbox:checked").each(function() {
        var cno = $(this).closest(".cart-item-container").data("cno");
        cnos.push(cno);
    });

    if (cnos.length === 0) {
        alert("삭제할 항목을 선택해주세요.");
        return;
    }

    if (confirm("선택한 상품들을 삭제하시겠습니까?")) {
        deleteCartItems(cnos); // 수집한 리스트를 보냄
    }
}

// 개별 상품 X 버튼 클릭 시
function deleteItemOne(obj, cno) {
    if (confirm("이 상품을 삭제하시겠습니까?")) {
        deleteCartItems([cno]);
    }
}
// 상품 총 금액 계산
function updateFinalTotal() {
    let totalSum = 0;

    // 최신화된 장바구니 총 합계 계산
    $(".item-total-price").each(function() {
        // data-value에 넣어둔 숫자값을 가져와서 더함
        let val = parseInt($(this).attr("data-value")) || 0;
        totalSum += val;
    });

    // 최종 금액 업데이트
    $("#total-sum").text(totalSum.toLocaleString() + "원");
}
