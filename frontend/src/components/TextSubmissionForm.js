import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import './TextSubmissionForm.css';
import * as Yup from 'yup';

function FormError(props) {
  return (
    <div className='form-error'>
      {props.children}
    </div>
  )
}

const initialValues = {
  language: '',
  text: ''
}

const onSubmit = (values, submitProps) => {
  console.log('Form data', values)
  console.log('submitProps', submitProps)
}

const validationSchema = Yup.object({
  language: Yup.string().required('Required!'),
  text: Yup.string().required("Required!")
})

function TextSubmissionForm () {
  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={onSubmit}
      validateOnMOunt
    >
      {formik => {
        console.log("Formik props: ", formik)
      return (
      <Form>
        <div className='form-control'>
          <label htmlFor='language'>Language</label>
          <Field
              as='select'
              id='language'
              name='language'>
            <option value="">Select...</option>
            <option value="spanish">Spanish</option>
            <option value="polish">Polish</option>
          </Field>
          <ErrorMessage name='language' component={FormError}/>
        </div>

        <div className='form-control'>
          <label htmlFor='text'>Text</label>
          <Field
            as='textarea'
            id='text'
            name='text'/>
          <ErrorMessage name='text'>
            {(errorMessage) => <div className='form-error'>{errorMessage}</div>}
          </ErrorMessage>
        </div>

        {/* <button type='submit'>Submit</button> */}
        <button
          type='submit'
          disabled={!formik.isValid
            || !formik.isSubmitting}>
          Submit
        </button>
      </Form>
      )
      }}
    </Formik>
  )
}

export default TextSubmissionForm;