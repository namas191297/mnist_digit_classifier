var loadFile = function(event) {
    var img = document.getElementById('display_image');
    img.src = URL.createObjectURL(event.target.files[0]);
    img.width = 300;
    img.height = 300;
  };