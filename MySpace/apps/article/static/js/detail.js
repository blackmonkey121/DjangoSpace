$(function () {
    // Add class 'son-img' to control the img overflow border.
    let $imgElem = $("#article-detail img");
    let $obj = $imgElem.parent('p')
    if ($obj){
        $obj.addClass('son-img')
    }
})