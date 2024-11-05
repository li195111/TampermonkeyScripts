
//驗證碼
$(document).on("click", "[id*='captcha_reload']", function (event) {
  event.preventDefault();
  $("[id*='captcha_image']").attr('src', "/captcha" + '/' + Math.random());
});

$("[id*='invite_verification']").val('74842')

$(document).on('submit', '#album_down', function (e) {
  $("#download_submit").attr('disabled', 'true');
  var aid = '190168'
  td_ga_tracker.doga_event('album_download', aid, 'Click', 1);
});

// 免等待
$(document).on("click", ".triggerpop", function (event) {
  if ($.cookie('zone-cap-4082952') >= 3) {
    var popurl = 'https://98pro.cc/JeqMxL'
    $(this).attr('href', popurl).attr('rel', 'noopener nofollow').attr('target', '_blank');
  }
  $(this).hide();
  $('.text-center.m-b-10').text("可以下載囉！");
  $('.down').find('.col-lg-6.col-md-6.col-sm-6').show();
});


//倒數
var s = document.getElementById("timer");

function run() {
  if (s.innerHTML == 0) {
    $('.triggerpop').hide();
    $('.down').find('.col-lg-6.col-md-6.col-sm-6').show();
    $('.text-center.m-b-10').text("可以下載囉！");
    return false;
  }
  s.innerHTML = s.innerHTML * 1 - 1;
}

window.setInterval("run();", 1000);

<form action="" method="post" name="album_down" id="album_down">
  <div class="col-lg-6 col-md-6 col-sm-6" style="">
    <img src="/captcha/0.4671161610448685" id="captcha_image" alt="Are you human?">
      <a href="#reload_captcha" style="display: inline-block;" id="captcha_reload">換一張驗證圖 </a>
  </div>
  <div class="col-lg-6 col-md-6 col-sm-6" style="">
    <div class="input-group">
      <input type="hidden" name="album_id" value="191564">
        <input name="verification" type="text" class="form-control" value="" id="invite_verification" placeholder="請輸入圖片中的文字！ ">
          <span class="input-group-btn">
            <button type="submit" name="download_submit" id="download_submit" class="btn btn-primary">下載</button>
          </span>
        </div>
    </div>
</form>

