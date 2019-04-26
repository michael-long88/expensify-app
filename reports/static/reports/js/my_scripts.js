$(document).ready(function() {
    if ($("#netAmt").length > 0) {
        var net = $("#netAmt").text();
        net = Number(net);
        if(net <= 0) {
            $("#netAmt").addClass("net-red");
        } else if(net < 1000 && net > 0) {
            $("#netAmt").addClass("net-yellow");
        } else {
            $("#netAmt").addClass("net-green");
        }
    }

    if ($("#myModal").length > 0) {
        // Get the modal
        var modal = $("#myModal");

        // Get the image and insert it inside the modal
        var modalImg = $("#img01");

        $("#cat_breakdown_button").click(function(){
            $("#myModal").show();
            $("#img01").attr('src', '/static/reports/img/cat_breakdown.png');
        });

        // When the user clicks on <span> (x), close the modal
        $('.close').click(function() {
            $("#myModal").hide();
        });
    }
});