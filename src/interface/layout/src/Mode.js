import React, { Component } from 'react'
import {
    Form, FormGroup, Label, Button,
    Input
} from 'reactstrap';

import socket from './socket';
class Mode extends Component {
    constructor(props)
    {
        super(props);
        this.__onUpdate = this.__onUpdate.bind(this);
        this.__onReset = this.__onReset.bind(this);
    }

    componentDidMount()
    {
        this.input = document.getElementById("modes");
    }

    /**
     * @description
     * Cập nhật chế độ hoạt động
     */
    __onUpdate()
    {
        let code = this.input.selectedIndex;
        let desc = this.input.value;
        this.props.update({ desc, code });
    }

    /**
     * @description
     * Reset lại thiết bị
     */
    __onReset()
    {
        this.props.update({ desc : "chưa-xác-định", code : -1 });
        socket.emit("reset");
    }

    render() {
    return (
        <Form>
            <FormGroup>
            <Label for='modes'>Xác định cách phân loại:</Label>
            <Input 
                type='select' 
                name='modes' 
                id='modes'
            >
                <option>
                    Dựa vào rau củ
                </option>
                <option>
                    Dựa vào rác thải
                </option>
                <option>
                    Dựa vào màu sắc
                </option>
                <option>
                    Dựa vào kích cỡ
                </option>
            </Input>
            </FormGroup>
            <FormGroup>
            <Button 
                block color='danger' 
                onClick={this.__onUpdate}
            >
                Cập nhật chế độ
            </Button>
            </FormGroup>
            <FormGroup>
            <Button 
                block color='warning'
                onClick={this.__onReset}
            >
                Khởi động lại
            </Button>
            </FormGroup>
        </Form>
    )
  }
}

export default Mode;