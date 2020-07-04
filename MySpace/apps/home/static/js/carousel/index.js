//banner 轮播图滑动
$('.index_banner').slick({
    autoplay: true,
    arrows: false,
    dots:false,
    infinite: true,
    speed: 500,
    autoplaySpeed: 5000,
    pauseOnHover: false,
    fade: true,
    responsive: [
      {
        breakpoint: 992,
        settings: {
          dots: true
        }
      }
    ]
});

// 轮播图底部样式
$('.index_banner').init(function(slick){
    $('.index_banner .item.slick-current').addClass('active').siblings().removeClass('active')
})
$('.index_banner').on('afterChange',function(slick,currentSlide){
    $('.index_banner .item.slick-current').addClass('active').siblings().removeClass('active');
    var _index = $('.index_banner').slick('slickCurrentSlide')
    $('.section1 .number span').eq(_index).addClass('active').siblings().removeClass('active')
})

$('.section1 .number span').click(function(){
    var _index = $(this).index();
    $('.index_banner').slick('slickGoTo',_index);
    $(this).addClass("active").siblings().removeClass("active")
});
$('.section1 .prev').click(function(){
  $('.index_banner').slick('slickPrev')
})
$('.section1 .next').click(function(){
  $('.index_banner').slick('slickNext');
});

//全屏滚动
$('#index_main').fullpage({
	'navigation': true,
	slidesNavigation: true,
	controlArrows: false,
	continuousHorizontal:true,
	scrollingSpeed:1000,
	showActiveTooltip :true,
	anchors: ['zero', 'one', 'two', 'three', 'four'],
	loopHorizontal: true,
	afterLoad: function(anchorLink, index){
		if(index == 1){
			$('header').removeClass('on');
		}
		if(index == 2){
			$('header').addClass('on');
			$('.section2 .page-btn').show().addClass('animated fadeInUp').css('animation-delay', '.1s');
		}
		if(index == 3){
			$('header').addClass('on');
			$('.section3 .page-btn').show().addClass('animated fadeInUp').css('animation-delay', '.1s');
		}
		if(index == 4){
			$('header').addClass('on');
			$('.section4 .page-btn').show().addClass('animated fadeInUp').css('animation-delay', '.1s');
		}
		if(index == 5){
			$('header').addClass('on');
			$('.section5 .page-btn').show().addClass('animated fadeInUp').css('animation-delay', '.1s');
		}
	},
	onLeave: function(index, direction){
	}
})