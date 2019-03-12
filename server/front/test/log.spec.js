import { mount } from '@vue/test-utils';
import log from '@/components/Landing/login.vue';
import Vue from '../node_modules/vue';

describe('show值改变', () => {
  const wrapper = mount(log);
  it('提交密码', () => {
    expect(wrapper.vm.currValue).toBe('0');
    wrapper.vm.currValue = '5';
    wrapper.vm.isSpace = false;
  });
  it('before change', () => {
    expect(wrapper.vm.show).toBe(true);
    expect(wrapper.vm.count).toBe('');
  });
  it('after change', () => {
    const button = wrapper.find('el-button');
    button.trigger('click');
    expect(wrapper.vm.show).toBe(false);
    expect(wrapper.vm.count).toBe(60);
  });
});

describe('login.vue', () => {
  const wrapper = mount(log);
  wrapper.vm.currValue = '5';
  it('属性', () => {
    const tabs = wrapper.find('el-button');
    expect(tabs.text()).toBe('发送验证码');
  });
});

describe('login.vue', () => {
  const wrapper = mount(log);
  it('watch the value in login page', (done) => {
    wrapper.vm.initial = '2';
    Vue.nextTick(() => {
      expect(wrapper.vm.currValue).toBe('3');
    });
    wrapper.vm.initial = '3';
    Vue.nextTick(() => {
      expect(wrapper.vm.currValue).toBe('3');
      done();
    });
  });
});
