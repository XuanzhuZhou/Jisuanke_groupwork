import { mount } from '@vue/test-utils';
import register from '@/components/Landing/register.vue';

describe('register.vue', () => {
  const wrapper = mount(register);
  wrapper.vm.currValue = '6';
  wrapper.vm.isSpace = false;
  it('before change code', () => {
    expect(wrapper.vm.show).toBe(true);
    expect(wrapper.vm.count).toBe('');
  });
  it('after change code', () => {
    const button = wrapper.findAll('el-button').at(0);
    button.trigger('click');
    expect(wrapper.vm.show).toBe(false);
    expect(wrapper.vm.count).toBe(60);
  });
});
