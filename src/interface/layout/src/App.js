import React, { Component } from 'react'
import {
  Row, Col,
  Container, List
} from 'reactstrap';

import './App.css';
import Image from './Image';
import Mode from './Mode';

import socket from './socket';
class App extends Component {
  constructor(props)
  {
    super(props);

    this.__onMode = this.__onMode.bind(this);
    
    /// Lắng nghe sự kiện từ server
    socket.on("update-stack", r => this.__updateStack(r));
    socket.on("update-classification", c => this.__updateClassification(c));
  }

  /**
   * 
   * @param {*} param0
   * @default
   * Cập nhật chế độ hoạt động 
   */
  __onMode({ desc, code })
  {
    this.mode.innerText = desc;
    socket.emit("update-mode", code);
  }

  /**
   * 
   * @param {*} param0
   * @description
   * Tiến hành cập nhật số hàng hóa vào kho 
   */
  __updateStack({ yellow_stack, blue_stack, undefined_stack })
  {
    /// Chuỗi giá trị { yellow_stack : "", blue_stack : "", undefined_stack : "" }
    this.yellow_stack.innerText = yellow_stack;
    this.blue_stack.innerText = blue_stack;
    this.undefined_stack.innerText = undefined_stack;
  }

  /**
   * 
   * @param {*} content
   * @description
   * Tiến hành thêm kết quả nhận dạng 
   */
  __updateClassification(content)
  {
    let { msg, res } = content;
    console.log(content);
  }

  /**
   * @description
   * Cập nhật các giá trị cần thiết
   */
  componentDidMount()
  {
    this.yellow_stack = document.getElementById("yellow-stack");
    this.blue_stack = document.getElementById("blue-stack");
    this.undefined_stack = document.getElementById("undefined-stack");
    this.list = document.getElementById("working-time");
    this.mode = document.getElementById("mode");
  }

  render() {
    return (
      <Container>
        <h2 className='text-center title text-bold' >DỰ ÁN ROBOT BĂNG CHUYỀN TỰ ĐỘNG</h2>
        <Row >
          <Col className='camera-layout'>
            <Image />
          </Col>
          <Col className='content-layout' >
            {/* Chế độ + Nội dung */}
            <h4 className='text-center' >Chế độ hoạt động và kết quả</h4>
            <Row>
              <Col>
                <h5 className='text-center' >Kết quả nhận dạng</h5>
                <List className='classification-result' id='working-time'></List>
              </Col>
              <Col>
                <h5 className='text-center' >Chế độ</h5>
                <h6 style={{
                  color : "red"
                }} > Chế độ hoạt động: <span style={{ color : "blue" }} id="mode" >chưa-xác-định</span> </h6>
                <Mode update={this.__onMode} />
              </Col>
            </Row>

            {/* QUản lí */}
            <h5 className='text-center'>Quản lí hàng hóa (số hàng hóa vào kho)</h5>
            <Row>
              <Col>
                <h6 className='text-center' style={{ color : "orange" }} >Ngăn màu vàng</h6>
                <div className='manage' id='yellow-stack' ></div>
              </Col>
              <Col>
                <h6 className='text-center' style={{ color : "blue" }} >Xanh dương</h6>
                <div className='manage' id='blue-stack' ></div>
              </Col>
              <Col>
                <h6 className='text-center' >Không xác định</h6>
                <div className='manage' id='undefined-stack' ></div>
              </Col>
            </Row>
          </Col>
        </Row>
      </Container>
    )
  }
}

export default App;