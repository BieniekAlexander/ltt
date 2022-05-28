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

const validationSchema = Yup.object({
  language: Yup.string().required('Required!'),
  text: Yup.string().required("Required!")
})

function TextSubmissionForm(props) {
  return (
    // <div>
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={props.handleClick}
      validateOnMOunt
      {...props}
    >
      {formik => {
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
            name='text'
            // style={{width: "150%", height: "250px"}}
            />
          <ErrorMessage name='text'>
            {(errorMessage) => <div className='form-error'>{errorMessage}</div>}
          </ErrorMessage>
        </div>

        <button
          type='submit'
          disabled={!formik.isValid
            || formik.isSubmitting
          }
        >
          Submit
        </button>
      </Form>
      )
      }}
    </Formik>
    // </div>
  )
}

export default TextSubmissionForm;