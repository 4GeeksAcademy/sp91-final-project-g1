import React from "react";

export const Settings = () => {

    return (
        <div className="text-center mt-2">
            <h1>Hola, Marcos</h1>
            <form>
                <div class="form-group">
                    <label for="formGroupExampleInput">Username</label>
                    <input type="text" class="form-control" id="formGroupExampleInput1" placeholder="Example input" />
                </div>
                <div class="form-group">
                    <label for="formGroupExampleInput2">Email</label>
                    <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Another input" />
                </div>
                <div class="form-group">
                    <label for="formGroupExampleInput2">Password</label>
                    <input type="password" class="form-control" id="formGroupExampleInput3" placeholder="Another input" />
                </div>
                <div class="form-group">
                    <label for="formGroupExampleInput2">Phone number</label>
                    <input type="text" class="form-control" id="formGroupExampleInput4" placeholder="Another input" />
                </div>
            </form>
        </div>
    )
}