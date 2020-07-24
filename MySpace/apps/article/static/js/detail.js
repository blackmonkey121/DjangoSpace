// 头像URL：/static/img/AVATAR.png
$(function () {
    // Add class 'son-img' to control the img overflow border.
    let $imgElem = $("#article-detail img");
    let $obj = $imgElem.parent('p')
    if ($obj) {
        $obj.addClass('son-img')
    }
    // 格式化时间
    function getCurrentDate(date) {
        var y = date.getFullYear();
        var m = date.getMonth() + 1;
        var d = date.getDate();
        var h = date.getHours();
        var min = date.getMinutes();
        var str = y + '年' + (m < 10 ? ('0' + m) : m) + '月' + (d < 10 ? ('0' + d) : d) + '日  ' + (h < 10 ? ('0' + h) : h) + ':' + (min < 10 ? ('0' + min) : min);
        return str;
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
            let lid = cls.substring(1, 2) - 1

            list[i].setAttribute('id', elemId + '-link');

            let $cttElem = $('<p></p>').attr('class', 'cls' + '-' + cls).text($(list[i]).text()).attr('data-href', '#' + elemId + '-link')
            $content.append($cttElem)

        }
    }

    createContent()

    // Top title
    $('#ctt-body p').click(function (e) {
        e.preventDefault();
        var jumpId = $(this).data('href');
        $('body, html').animate({scrollTop: $(jumpId).offset().top}, 'slow');
    });

    // close content
    $('#ctt-head i').click(function () {
        $contentSidebar.slideToggle()
    })

    // close left block
    $('.rlt-head i').click(function () {
        $(this).toggleClass('fa-minus').toggleClass('fa-chevron-down').parent().parent().find('.rlt-body').slideToggle()
    })

    // Show content
    $('#showContent').click(function () {
        $contentSidebar.slideToggle()
    })

    // Show To Page Top
    $(window).scroll(function () {
        if ($(window).scrollTop() > 1000) {
            $('#toTop').fadeIn();
        } else {
            $('#toTop').fadeOut();
        }
    });

    // To Page Top
    $("#toTop").click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 1000);
        return false;
    });

    // count textarea word
    let $commentElem = $('#comment-text')
    $commentElem.on('input propertychange', function () {
        $('#num-word').text($(this).val().length)
    })

    // commit comment
    $('#post-btn').on('click', function () {

        let $sendData = {
            'context': $commentElem.val(),
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
        }

        $.ajax({
            url: '/comment/article/' + $('#page_data').data('article_id') + '/',
            data: $sendData,
            dataType: 'json',
            type: 'post',

            before: function () {
                console.log('commit flag')
            },

            success: function (data) {
                if (data.status) {
                    console.log('ok')
                    // 前端插入评论
                    let $newElements = $('<div class="cmt_line">' +
                        '<div class="cmt_avatar">' +
                        '<img src="/static/img/AVATAR.png" alt="">' +
                        '</div>' +
                        '<div class="cmt_right">' +
                        '<div class="cmt_text">' + $sendData.context + '</div>' +
                        '</div>' +
                        '<div class="cmt_footer">' +
                        '<span hidden></span>' +
                        '<span class="cmt_time"><i class="fa fa-clock-o" aria-hidden="true"></i> ' + getCurrentDate(new Date())+ '</span>' +
                        '<span></span>' +
                        '</div>' +
                        '</div>')
                    $newElements.hide()
                    $('#comment').prepend($newElements)
                    $newElements.slideDown(300)

                    // 清空评论框信息 和 字符统计信息
                    $commentElem.text('')
                    $('#num-word').text('0')

                } else {
                    console.log('error')
                    console.log(data.msg)

                }
            },
            error: function () {

            }
        })

    })

})