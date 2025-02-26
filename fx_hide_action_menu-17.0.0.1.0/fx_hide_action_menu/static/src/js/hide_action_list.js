/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {ListController} from "@web/views/list/list_controller";
import {useService} from "@web/core/utils/hooks";

patch(ListController.prototype, {
    /**
     * @override
     */

    async setup() {
        super.setup();
        this.orm = useService("orm");

        const currentUser = await this.orm.call(
            "res.users",
            "get_is_hide_action_and_applied_models"
        );
        this.is_hide_action = currentUser.is_hide_action;
        this.applied_models = currentUser.applied_action_models_ids;

        if (
            this.props.resModel &&
            this.applied_models.some(
                (modelData) => modelData[1] === this.props.resModel
            )
        ) {
            self.model = this.props.resModel;
        }
    },

    get actionMenuItems() {
        const actionMenus = super.actionMenuItems;

        if (this.props.resModel === self.model) {
            const {action} = actionMenus;

            actionMenus.action = [];
        }

        if (this.is_hide_action) {
            const {action} = actionMenus;

            actionMenus.action = [];
        }

        return actionMenus;
    },
});
