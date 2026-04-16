// ajax 통신으로 로그인 처리
window.onload = function()
{
    window.scrollTo(0, 0);
    
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
	
	$("#FrmSubmit").on("submit", function(e){
    	e.preventDefault(); //새로고침 방지
    	searchKeyword();
	});
}

// 시간대에 맞게 화면에 출력
$(document).ready(function() {

    // 현재 시간 가져오기
    var nowHour = new Date().getHours();
    var TimeText = "";

    // 시간대 조건문
    if (nowHour >= 7 && nowHour < 11) {
        TimeText = "상쾌한 아침이에요! 추천 메뉴 확인하세요.";
        $("#keyword").attr("placeholder", " 아침 뭐 먹지?");
    } else if (nowHour >= 11 && nowHour < 16) {
        TimeText = "즐거운 점심 식사! 인기 메뉴 어때요?";
        $("#keyword").attr("placeholder", " 점심 뭐 먹지?");
    } else if (nowHour >= 16 && nowHour < 20) {
        TimeText = "고단한 하루의 끝, 맛있는 저녁 한 끼 어때요?";
        $("#keyword").attr("placeholder", " 저녁 뭐 먹지?");
    } else {
        TimeText = "야식이 생각나는 밤, 지금 핫한 메뉴는?";
        $("#keyword").attr("placeholder", " 야식 뭐 먹지?");
    }

    $("#time-text").text(TimeText);
});

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
   	data : {target : target},
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
   });
}


function ShowItem(target) 
{
    $.ajax({
    	url : "/recommend.do",
    	type : "get",
    	dataType: "json",
    	data : {target : target},
    	async : true,
    	success : function(reco_dict) 
    	{
        	let html = "";

            reco_dict.forEach(function(item) 
            {
                html += `
                    <div class="col-6 col-md-3">
                        <a href="/view.do?code=${item.code}">
                            <div class="product-card">
                                <img src="${item.image}">
                                <div class="product-name">${item.item_name}</div>
                                <div class="product-price">${item.price}</div>
                            </div>
                        </a>
                    </div>
                `;
            });
            $('#reco_items').html(html);
            
            window.scrollTo(0, document.body.scrollHeight);
    	},
    	error : function(request, status, error) 
    	{
        	alert("실패");
    	}
    });
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
                
            } else if(response.result === "login"){
                alert(response.message);
            } else if(response.result === "duplicate"){
                alert(response.message);
            } else if(response.result === "duplicate"){
                alert(response.message);
            } else{
                alert("장바구니 담기 실패!");
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
    var container = $(obj).closest(".cart-item-container");
    var cno = container.attr("data-cno");
    var qtyCount = $(obj).siblings(".qtyCount")
    var count    = parseInt(qtyCount.text());
    
    if(count > 1)
    {
        count -= 1;
        qtyCount.text(count);
        if(typeof cno != "undefined"){
            updateQty(cno, count);
        }
    }
}
// 수량 증가
function QtyPlus(obj)
{
    var container = $(obj).closest(".cart-item-container");
    var cno = container.attr("data-cno");
    var qtyCount = $(obj).siblings(".qtyCount")
    var count    = parseInt(qtyCount.text());
    
    count += 1;
    qtyCount.text(count);
    if(typeof cno != "undefined"){
        updateQty(cno, count);
    }
}

function updateQty(cno, count)
{
    $.ajax({
        url: '/update_cart_qty.do', // 본인의 서버 엔드포인트에 맞게 수정
        method: 'POST',
        data: {
            cno: cno,
            qty: count
        },
        success: function(data) {
            
            if(data == "success"){
                updateFinalTotal();
            } else{
                alert("수량 변경에 실패했습니다.");
            }
            
        },
        error: function(err) {
            alert("수량 변경에 실패했습니다.");
        }
    });
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
                    $(".cart-summary-item[data-cno='" + cno + "']").remove();
                    $("#cart-badge").text(response.new_count);
                    updateFinalTotal();
                    if (response.new_count == 0) {
                        $("#cart-badge").val(0);
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

    // 최신화된 장바구니 총 합계 계산
    let totalSum = 0;

    // 모든 상품 컨테이너를 하나씩 확인
    $(".cart-item-container").each(function() {
        // 체크박스 체크되어 있는지 확인
        let cno = $(this).attr("data-cno");
        let qty = parseInt($(this).find(".qtyCount").text());
        let unitPrice = parseInt($(this).data("price"));
        let isChecked = $(this).find(".item-checkbox").prop("checked");
        let summaryItem = $(".cart-summary-item[data-cno='" + cno + "']");

        if (isChecked) {
        
            summaryItem.find(".small").text(unitPrice.toLocaleString() + "원 x " + qty);
            let itemTotal = unitPrice * qty;
            
            // 체크된 경우에만 금액을 더함
            let val = summaryItem.find(".item-total-price").attr("data-value");
            
            totalSum += itemTotal;
            summaryItem.show();
            
        }else{
            summaryItem.hide();
        }
    });

    // 최종 금액 업데이트
    $("#total-sum").text(totalSum.toLocaleString() + "원");
}

// 체크박스 클릭 시 합계 업데이트
$(document).on("change", ".item-checkbox", function() {
    updateFinalTotal();
});

// 전체 선택 체크박스 클릭 시 합계 업데이트 (있을 경우)
$(document).on("change", "#selectAll", function() {
    // 전체 선택 클릭 시 브라우저가 체크박스 상태를 바꿀 시간을 약간 줌
    setTimeout(updateFinalTotal, 10);
});

// 검색&카테고리 목록부분
let currentCategory = 0
let categoryTitle   = ""
let keyword = ""
let keywordTitle = ""
// 카테고리 선택 시
function selectCategory(element)
{
    // 클릭 시 글자 굵게
    $(".cat-item").removeClass('fw-bold');
    $(element).addClass('fw-bold');
    categoryTitle = $(element).text();
    
    currentCategory = $(element).data('value');
    keyword = ""
    loadItems(currentCategory, 1);
}

// 페이지 번호 클릭 시
function changePage(page) {
    loadItems(currentCategory, page);
}

$(document).ready(function() {
    $(".filter-btn").on("click", function() {
        // 클릭한 버튼 -> active 클래스 추가, 나머지는 제거
        $(".filter-btn").removeClass("active");
        $(this).addClass("active");

        // 선택된 기간 값 -> all(전체), 1m(1달), 3m(3달)
        const period = $(this).data("period");

        // 페이징
        location.href = "/purchase.do?page=1&period=" + period;
    });
});

// 검색 시
function searchKeyword() {
    keyword = $("#keyword").val();
    keywordTitle = "[" + keyword + "] 관련 상품"
    currentCategory = 0
    loadItems(currentCategory, 1, keyword);
}

// 실제 AJAX 실행 함수
function loadItems(category, page, keyword) {
    $.ajax({
    	url : "/navi.do",
    	type : "get",
    	dataType: "html",
    	data :
    	{
        	category : category,
        	page     : page,
        	keyword  : keyword
    	},
    	async : true,
    	success : function(data) 
    	{
            $("#category").html(data);
            if (keyword) {
                $("#category-title").html(keywordTitle);
            }
            else if (categoryTitle) {
                $("#category-title").html(categoryTitle);
            }
            else{
                $("#category-title").html("전체보기");
            }
            
            
            //페이지 상단으로 스크롤 부드럽게 이동
            window.scrollTo({top: 830, behavior: 'smooth'});
    	},
    	error : function(request, status, error) 
    	{
        	alert("실패");
    	}
    });
}

function purchase(){
    let purchaseData = [];
    
    $(".cart-item-container").each(function() {
        let isChecked = $(this).find(".item-checkbox").prop("checked");
        
        if (isChecked) {
            let cno = $(this).attr("data-cno");               // 장바구니 번호
            let code = $(this).find("#item-code").val();      // 상품 코드
            let qty = $(this).find(".qtyCount").text();       // 수량 (텍스트박스라면 .val())
            
            purchaseData.push({
                cno  : cno,
                code : parseInt(code),
                qty  : parseInt(qty)
            });
        }
    });
    
    // 체크된 상품이 없을 때
    if (purchaseData.length === 0) {
        alert("구매할 상품을 선택해주세요.");
        return;
    }
    
    $.ajax({
        url: "/purchase.do",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            items: purchaseData
        }),
        success: function(data) {
            if (data == "success") {
                alert("결제가 완료되었습니다!");
                
                location.href = "/purchase.do"; // 완료 페이지로 이동
            } else {
                alert("구매 처리 중 오류가 발생했습니다.");
            }
        },
        error: function() {
            alert("서버 통신 오류가 발생했습니다.");
        }
    });
}
