import { mount } from '@vue/test-utils';
import aboutUs from '@/components/Landing/aboutUs.vue';
import Vue from '../node_modules/vue';

describe('aboutUs.vue', () => {
  const wrapper = mount(aboutUs);
  it('watch the initial and change currValue', (done) => {
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
