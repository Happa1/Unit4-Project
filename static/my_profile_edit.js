$('#form').on('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $("#img").attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});

// 削除ボタンクリック時にフォームとプレビューを初期化
$('#delete').on('click', function (e) {
  $("#img").attr('src', '/static/profile_image/blank_user.jpeg');
  $("#form").val('');
});