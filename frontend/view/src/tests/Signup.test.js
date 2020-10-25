import Signup from '../Signup.js';
import React from 'react';
import renderer from 'react-test-renderer';
import { BrowserRouter } from 'react-router-dom';

test('snapshot headjs renders', () => {
  const component = renderer.create(<headjs counter={1} />);
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});


test('snapshot midpart renders', () => {
  const component = renderer.create(<midpart counter={1} />);
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

test('snapshot formblock renders', () => {
  const component = renderer.create(<formblock counter={1} />);
  let tree = component.toJSON();
  expect(tree).toMatchSnapshot();
});

