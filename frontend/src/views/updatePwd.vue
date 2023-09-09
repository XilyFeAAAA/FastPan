<script>
import { defineComponent } from 'vue'
import Swal from 'sweetalert2'
import Request from '../utils/Request.js'

const api = {
    updatePassword: 'user/resetPwd-auth',
}
export default defineComponent({
    methods: {
        async showChangePasswordDialog() {
            await Swal.fire({
                title: 'Change Password',
                html:
                    '<div class="flex-center flex-column">' +
                    '<input id="swal-input-password" class="my-input-class" type="password" placeholder="New Password" autocomplete="new-password">' +
                    '<input id="swal-input-confirm-password" class="my-input-class" type="password" placeholder="Confirm Password" autocomplete="new-password">' +
                    '</div>',

                confirmButtonText: 'Confirm',
                showCancelButton: true,
                cancelButtonText: 'Cancel',
                customClass: {
                    input: 'my-input-class',
                },
                reverseButtons: true,
                showCloseButton: false,
                focusConfirm: false,
                preConfirm: () => {
                    const password = document.querySelector('#swal-input-password').value
                    const confirmPassword = document.querySelector(
                        '#swal-input-confirm-password',
                    ).value

                    if (!password) {
                        Swal.showValidationMessage('Please enter new password')
                    } else if (password !== confirmPassword) {
                        Swal.showValidationMessage('Passwords do not match')
                    } else {
                        const res = Request.post(api.updatePassword, {
                            password: password,
                        })
                        if (res) {
                            Swal.fire({
                                toast: true,
                                position: 'top-end',
                                showConfirmButton: false,
                                timer: 3000,
                                type: 'success',
                                title: 'Successfully Update',
                            })
                        }
                    }
                },
            })
        },
    },
})
</script>

<style lang="scss">
.my-input-class {
    width: 70%;
    &:not(:last-of-type) {
        margin-bottom: 10px;
    }
}
</style>
