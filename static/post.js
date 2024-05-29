// document.addEventListener('DOMContentLoaded', function() {
//
//    // ▼サブBOXを全て非表示にする
//    var allSubBoxes = document.getElementsByClassName("sub_select");
//    for( var i=0 ; i<allSubBoxes.length ; i++) {
//       allSubBoxes[i].style.display = 'none';
//    }
//
//    // ▼全てのプルダウンボックスごとに処理
//    var mainBoxes = document.getElementsByClassName('pulldownset');
//    for( var i=0 ; i<mainBoxes.length ; i++) {
//
//       var mainSelect = mainBoxes[i].getElementsByClassName("main_select");   // メインのプルダウンメニュー（※後でvalue属性値を参照するので、select要素である必要があります。）
//       mainSelect[0].onchange = function () {
//          // ▼同じ親要素に含まれている全サブBOXを消す
//          var subBox = this.parentNode.getElementsByClassName("sub_select");   // 同じ親要素に含まれる.subbox（※select要素に限らず、どんな要素でも構いません。）
//          for( var j=0 ; j<subBox.length ; j++) {
//             subBox[j].style.display = 'none';
//          }
//
//          // ▼指定されたサブBOXだけを表示する
//          if( this.value ) {
//             var targetSub = document.getElementById( this.value );   // 「メインのプルダウンメニューで選択されている項目のvalue属性値」と同じ文字列をid属性値に持つ要素を得る
//             targetSub.style.display = 'inline';
//          }
//       }
//
//    }
//
// });

document.addEventListener('DOMContentLoaded', function() {
    // Hide all sub select boxes initially and remove their name attributes
    var allSubBoxes = document.getElementsByClassName("sub_select");
    for (var i = 0; i < allSubBoxes.length; i++) {
        allSubBoxes[i].style.display = 'none';
        allSubBoxes[i].removeAttribute('name'); // Ensure name attribute is removed
    }

    // Process each pulldown set
    var mainBoxes = document.getElementsByClassName('pulldownset');
    for (var i = 0; i < mainBoxes.length; i++) {
        var mainSelect = mainBoxes[i].getElementsByClassName("main_select")[0]; // Get the main select element
        if (mainSelect) { // Check if mainSelect is found
            mainSelect.onchange = function () {
                // Hide all sub select boxes within the same pulldown set and remove their name attributes
                var subBoxes = this.parentNode.getElementsByClassName("sub_select");
                for (var j = 0; j < subBoxes.length; j++) {
                    subBoxes[j].style.display = 'none';
                    subBoxes[j].removeAttribute('name'); // Remove name attribute
                }

                // Show the selected sub select box and set its name attribute
                if (this.value) {
                    var targetSub = document.getElementById(this.value);
                    if (targetSub) { // Check if targetSub is found
                        targetSub.style.display = 'inline';
                        targetSub.setAttribute('name', 'subject'); // Set the name attribute
                    }
                }
            }
        }
    }
});


$('#form').on('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $("#img").attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});

// 削除ボタンクリック時にフォームとプレビューを初期化
$('#delete').on('click', function (e) {
  $("#img").attr('src', '/static/image/upload_img.jpeg');
  $("#form").val('');
});