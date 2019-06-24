import axios from 'axios/index'

export const HTTP = axios.create({
    baseURL: "http://localhost:5000/api/"
});


export const globalLoadDecorator =  (wrapped) => {
  return function() {
    console.log('Starting');
    const result = wrapped();
    console.log('Finished');
    return result;
  }
};