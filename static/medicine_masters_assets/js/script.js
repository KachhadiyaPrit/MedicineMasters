import { Modal, Ripple, initMDB } from "mdb-ui-kit";

initMDB({ Modal, Ripple });

import { Carousel, initMDB } from "mdb-ui-kit";

initMDB({ Carousel });

import { Tab, initMDB } from "mdb-ui-kit";

initMDB({ Tab });

$("#edit_profile_btn").click(
    function(){
        $("#edit_user_detail").removeClass("d-none").addClass("d-block");
        $("#user_detail").removeClass("d-block").addClass("d-none");
    }
);