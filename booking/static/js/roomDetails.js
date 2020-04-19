"use strict";

$(document).ready(function () {
        let rooms = $(".room-details").length;
        console.log(rooms);
        for (let i = 1; i < rooms + 1; i++) {
            //     console.log(i);
            //     console.log($(`.room-details-${i} th`));
            //
            //     $(`.room-details-${i} th`).tooltip({
            //         content:
            //             `<div class="room_description-tooltip">
            //             <h4>${$(`.room-details-${i}`).data("name")}</h4>
            //             <h4>${$(`.room-details-${i}`).data("description")}</h4>
            //             <img src="${$(`.room-details-${i}`).data("image")}">
            //         </div>`
            //     });
            // }
            $(`.room-details-${i} th`).each(function () {
                console.log(this);
                $(this).tooltip({
                    content:
                        `<div class="room_description-tooltip">
                             <h4>${$(`.room-details-${i}`).data("name")}</h4>
                             <h4>${$(`.room-details-${i}`).data("description")}</h4>
                             <img src="${$(`.room-details-${i}`).data("image")}">
                         </div>`
                });
            })
        }
    }
);