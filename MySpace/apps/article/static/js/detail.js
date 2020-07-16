$(function () {
    // Add class 'son-img' to control the img overflow border.
    let $imgElem = $("#article-detail img");
    let $obj = $imgElem.parent('p')
    if ($obj) {
        $obj.addClass('son-img')
    }

    // create content
    let $contentSidebar = $('#contentSidebar')
    let $titleClass = ['h2', 'h3', 'h4']    // 目录元素
    let $content = $('#ctt-body')    // 目录主体
    let guidStr = 'hid'   // 目录索引 头

    function createContent() {
        let list = $($titleClass.join())  // 获取元素

        for (let i = 0; i < list.length; i++) {

            let cls = list[i].tagName.toLowerCase()
            let elemId = guidStr + cls + '-' + i;
            let lid = cls.substring(1,2) - 1

            list[i].setAttribute('id', elemId + '-link');

            let $cttElem = $('<p></p>').attr('class', 'cls' + '-' + cls).text($(list[i]).text()).attr('data-href', '#' + elemId + '-link')
            $content.append($cttElem)

        }
    }
    createContent()

    // Top title
    $('#ctt-body p').click(function(e){
  	e.preventDefault();
	var jumpId = $(this).data('href');
	$('body, html').animate({scrollTop: $(jumpId).offset().top}, 'slow');
});

    // close content
    $('#ctt-head i').click(function () {
        $contentSidebar.fadeOut()
    })

    // Show content
    $('#showContent').click(function () {
        $contentSidebar.fadeToggle()
    })

    // Show To Page Top
        $(window).scroll(function(){
        if($(window).scrollTop() > 1000){
            $('#toTop').fadeIn();
        }else{
            $('#toTop').fadeOut();
        }
    });

    // To Page Top
        $("#toTop").click(function() {
        $('body,html').animate({
            scrollTop: 0
        },1000);
        return false;
    });
})