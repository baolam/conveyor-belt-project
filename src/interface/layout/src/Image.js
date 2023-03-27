import React, { Component } from 'react'

import socket from './socket';

class Image extends Component {
  componentDidMount()
  {
    this.image = document.getElementById("image");
    socket.on("streaming", (content) => {
      this.image.src = content;
    })
  }

  render() {
    return (
      <>
        {/* Cho camera */}
        <h4 className='text-center'>Dữ liệu từ camera</h4>
        <img 
          src='/camera.png' 
          alt='Ảnh từ camera' 
          className='image' 
          height={450} 
          id="image"
        />
      </>
    )
  }
}

export default Image;