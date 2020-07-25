    // <ul>
    // <li id="verify">
    //     <span>Verify Code</span> <input type="password" name="password" placeholder="Verify Code(6~18位)">
    //     <span id="verify-btn">verify</span>
    // </li>
    //     <li id="tips"><a href="mailto:931976722@qq.com"><span>Request Access:3213322480@qq.com</span></a></li>
    // </ul>

$(function () {
    $('#verify-btn').click(function () {
        let $pwd = $('#verify').find('input').val();
        alert($pwd)
    })
})