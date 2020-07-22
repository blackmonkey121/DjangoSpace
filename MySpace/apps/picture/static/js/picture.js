$(function () {
    var $data = $('#temp_data')    // 滚轮到页面底部 页面加载依赖该标签

    var $plat = $('#image_plat')

    var $image_list = $('#image-wall .image-line')

    // 新增图片
    var extendPicture = {

        // 随机数
        'rand': function (min, max) {
            return parseInt(Math.random() * (max - min + 1) + min);
        },

        // 添加元素样式
        'addStyle': function (elem) {
            $(elem).css({
                'margin': extendPicture.rand(80, 120) + 'px' + ' ' + extendPicture.rand(20, 80) + 'px',
                'display': 'inline-block',
            }).fadeIn('slow')

            $(elem).find('img').css({
                'height': extendPicture.rand(40, 200) + 'px'
            }).fadeIn('slow')
        },

        // 获取图片列表
        'getImageList': function (start, offset) {
            $.ajax({
                url: window.location,
                type: 'get',
                dataType: 'json',
                data: {
                    'start': start,
                    'offset': offset,
                    "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
                },

                beforeSend: function () {
                    console.log('send get image list flag')
                },

                success: function (data) {
                    if (data.status) {
                        // 获取到数据就添加照片
                        if (data.image_list.length) {

                            extendPicture.creatElement(data.image_list)

                        } else {
                            // 没有数据了就修改 flag 组织继续发送无关请求
                            $data.data('flag', 0)
                        }
                    } else {
                        // 失败继续发送
                        extendPicture.getImageList(start, offset)
                    }
                },

                error: function () {
                    alert("system exception!")
                }
            })

        },

        // 创建元素
        'creatElement': function (image_list) {
            for (let i = 0; i < image_list.length; i++) {

                let $elem =
                    $('<li class="image-line clearfix">' +
                    '<img src=' + image_list[i].thumbnail + ' alt=""' +
                        'rsrc=' + image_list[i].img +'>'+
                    '</li>')

                extendPicture.addStyle($elem)
                $('#image-wall').append($elem)
            }
        }

    }

    // 点击显示图片详情
    var showPicture = {
        'clickPicture': function (ths) {
            $plat.empty()
            let $thumb = $(ths).find('img')
            let $rurl = '/media/' + $thumb.attr('rsrc')
            let $img = $('<img src='+$rurl+' alt="">')

            // 父标签大小
            let $width = $plat.width()
            let $height = $plat.height()


            if ($thumb.width() > $thumb.height()){
                $img.css('width', $(window).width() * 0.63)
            }else {
                $img.css('height', $(window).height() * 0.63)
            }

            $('#image_plat').append($img).fadeIn('slow')

        }
    }

    // 第一页 缓慢显示
    $('#image-wall').fadeIn('slow')

    // 随机分配照片格式
    $image_list.each(function () {
        extendPicture.addStyle(this)
    })

    // 绑定照片的点击详情效果
    $(document).on('click','#image-wall .image-line', function () {
        showPicture.clickPicture(this)
    })

    // 点击关闭详情
    $plat.on('click', function () {
        $(this).fadeOut()
    })

    // 监听滚轮，边界自动加载下一页数据
    $("html").on('mousewheel', function(event){
        if ($(window).scrollTop() + $(window).height() >= $(document).height() && event.originalEvent.wheelDelta < 0) {
            let start = $data.data('start')
            let flag = $data.data('flag')
            // 判断请求标志位是否为真
            if (flag) {
                extendPicture.getImageList(start, 10)
            }
            // 请求起始位 + 10
            $data.data('start', start + 10)
        }
    });

    // 鼠标划过照片，显示desc 文本
    $image_list.on('mouseover', function () {

        $(this).find('span').fadeIn()
    })
    $image_list.on('mouseleave', function () {
        $(this).find('span').fadeOut()
    })

})