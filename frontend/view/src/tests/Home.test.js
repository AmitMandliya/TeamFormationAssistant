import Signup from '../Home.js';
import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter } from 'react-router-dom';

test('snapshot headjs renders', () => {
    const component = renderer.create(<headjs counter={1} />);
    let tree = component.toJSON();
    expect(tree).toMatchSnapshot();
  });