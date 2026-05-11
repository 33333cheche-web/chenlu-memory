Page({
  data: {
    noteId: '',
    note: {},
    isEdit: false,
    createTimeText: '',
    updateTimeText: ''
  },

  onLoad(options) {
    if (options.id) {
      this.setData({ noteId: options.id })
      this.loadNote()
    }
  },

  loadNote() {
    const notes = wx.getStorageSync('notes') || []
    const note = notes.find(n => n.id === this.data.noteId)
    
    if (note) {
      this.setData({
        note: note,
        createTimeText: this.formatTime(note.createTime),
        updateTimeText: this.formatTime(note.updateTime)
      })
    }
  },

  formatTime(timestamp) {
    const date = new Date(timestamp)
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
  },

  onInput(e) {
    this.setData({
      'note.content': e.detail.value
    })
  },

  toggleEdit() {
    if (this.data.isEdit) {
      // 保存
      this.saveNote()
    }
    this.setData({
      isEdit: !this.data.isEdit
    })
  },

  saveNote() {
    const notes = wx.getStorageSync('notes') || []
    const index = notes.findIndex(n => n.id === this.data.noteId)
    
    if (index !== -1) {
      notes[index].content = this.data.note.content
      notes[index].updateTime = Date.now()
      wx.setStorageSync('notes', notes)
      
      wx.showToast({
        title: '保存成功',
        icon: 'success'
      })
      
      this.loadNote()
    }
  },

  deleteNote() {
    wx.showModal({
      title: '确认删除',
      content: '删除后无法恢复，是否继续？',
      confirmColor: '#E53E3E',
      success: (res) => {
        if (res.confirm) {
          const notes = wx.getStorageSync('notes') || []
          const newNotes = notes.filter(n => n.id !== this.data.noteId)
          wx.setStorageSync('notes', newNotes)
          
          wx.showToast({
            title: '已删除',
            icon: 'success'
          })
          
          setTimeout(() => {
            wx.navigateBack()
          }, 1000)
        }
      }
    })
  },

  goBack() {
    wx.navigateBack()
  }
})