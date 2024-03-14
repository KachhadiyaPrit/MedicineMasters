$("#profiletxt").click(
    function(){
        $("#addresscard").removeClass("d-block").addClass("d-none");
        $("#address_link").removeClass("d-flex").addClass("d-none");
        $("#all_rewards_card").removeClass("d-flex").addClass("d-none");
        $("#profilecard").addClass("d-block").removeClass("d-none");
        $("#profile_link").addClass("d-flex").removeClass("d-none");
    }
);

$("#addresstxt").click(
    function(){
        $("#profilecard").removeClass("d-block").addClass("d-none");
        $("#profile_link").removeClass("d-flex").addClass("d-none");
        $("#all_rewards_card").removeClass("d-flex").addClass("d-none");
        $("#addresscard").addClass("d-block").removeClass("d-none");
        $("#address_link").addClass("d-flex").removeClass("d-none");
    }
);

$("#view_all_offers_txt").click(
    function(){
        $("#profilecard").removeClass("d-block").addClass("d-none");
        $("#profile_link").removeClass("d-flex").addClass("d-none");
        $("#addresscard").addClass("d-none").removeClass("d-block");
        $("#all_rewards_card").addClass("d-none").removeClass("d-block");
        $("#address_link").addClass("d-flex").removeClass("d-none");
    }
);

$("#edit_profile_btn").click(
    function(){
        $("#user_detail").removeClass("d-block").addClass("d-none");
        $("#delivery_address_card").removeClass("d-block").addClass("d-none");
        $("#edit_user_detail").removeClass("d-none").addClass("d-block");
    }
);

$("#profiletxt").click(
    function(){
        $("#user_detail").removeClass("d-none").addClass("d-block");
        $("#delivery_address_card").removeClass("d-block").addClass("d-none");
        $("#edit_user_detail").removeClass("d-block").addClass("d-none");
        $("#get_prescription").removeClass("d-block").addClass("d-none");
        $("#all_offer_card").addClass("d-none").removeClass("d-block");
        $("#all_rewards_card").addClass("d-none").removeClass("d-block");
    }
);

$("#addresstxt").click(
    function(){
        $("#user_detail").removeClass("d-block").addClass("d-none");
        $("#delivery_address_card").removeClass("d-none").addClass("d-block");
        $("#edit_user_detail").removeClass("d-block").addClass("d-none");
        $("#get_prescription").removeClass("d-block").addClass("d-none");
        $("#all_offer_card").addClass("d-none").removeClass("d-block");
        $("#all_rewards_card").addClass("d-none").removeClass("d-block");
    }
);

$("#edit_delivery_address").click(
    function(){
        $("#display_delivery_address").removeClass("d-block").addClass("d-none");
        $("#get_prescription").removeClass("d-block").addClass("d-none");
        $("#edit_address").removeClass("d-none").addClass("d-block");
        // $("#edit_user_detail").removeClass("d-block").addClass("d-none");
    }
);

$("#view_all_offers_txt").click(
    function(){
        $("#user_detail").removeClass("d-block").addClass("d-none");
        $("#delivery_address_card").removeClass("d-block").addClass("d-none");
        $("#edit_user_detail").removeClass("d-block").addClass("d-none");
        $("#get_prescription").removeClass("d-block").addClass("d-none");
        $("#all_offer_card").addClass("d-block").removeClass("d-none");
        $("#all_rewards_card").removeClass("d-block").addClass("d-none");
    }
);

$("#view_all_rewards_txt").click(
    function(){
        $("#user_detail").removeClass("d-block").addClass("d-none");
        $("#delivery_address_card").removeClass("d-block").addClass("d-none");
        $("#edit_user_detail").removeClass("d-block").addClass("d-none");
        $("#get_prescription").removeClass("d-block").addClass("d-none");
        $("#all_offer_card").addClass("d-none").removeClass("d-block");
        $("#all_rewards_card").addClass("d-block").removeClass("d-none");
    }
);

$("#get_prescription_txt").click(
    function(){
        $("#user_detail").removeClass("d-block").addClass("d-none");
        $("#delivery_address_card").removeClass("d-block").addClass("d-none");
        $("#edit_user_detail").removeClass("d-block").addClass("d-none");
        $("#all_offer_card").removeClass("d-block").addClass("d-none");
        $("#all_rewards_card").removeClass("d-block").addClass("d-none");
        $("#get_prescription").addClass("d-block").removeClass("d-none");
    }
);

$("#sign_up_btn").click(
    function(){
      $("#login").removeClass("d-block").addClass("d-none");
    }
  )