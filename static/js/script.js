$(document).ready(function () {
  $(".send-message-loader").hide();
  $(".owl-carousel").owlCarousel({
    loop: false,
    margin: 10,
    nav: false,
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 3,
      },
      1000: {
        items: 4,
      },
    },
  });
});

lang = $("html").attr("lang");

$("#lang")
  .children()
  .each(function () {
    if ($(this).attr("id") == lang) {
      $(this).removeClass("active");
      $(this).addClass("active");
    }
  });

function sendMessage() {
  $(".send-message-loader").show();
  language = $('html').attr('lang')
  email = $("#emailMessage").val();
  subject = $("#subjectMessage").val();
  msgTxt = $("#messageText").val();
  console.log(email, subject, msgTxt);
  $.ajax({
    url: "/sendMessage",
    method: "POST",
    data: {
      email: email,
      subject: subject,
      msgTxt: msgTxt,
      lang:language
    },
    
    success: function (response) {
      console.log(response["result"]);
      if (response["result"] == "success" || response['result'] == 'berhasil' ) {
        Swal.fire({
          title: response['result'],
          text: response["msg"],
          icon: "success",
        }).then(function () {
          location.reload();
        });
      }else{
        Swal.fire({
          title: response['result'],
          text: 'please try again',
          icon: "error",
        }).then(function () {
          $(".send-message-loader").hide();
        });
      }
    },
  });
}
