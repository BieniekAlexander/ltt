import React from 'react';
import { useFormik } from 'formik';
import './TextSubmissionForm.css';
import * as Yup from 'yup';

function TextSubmissionForm() {
  const initialValues = {
    language: '',
    text: ''
  }

  const onSubmit = values => {
    console.log('Form data', values)
  }

  const validationSchema = Yup.object({
    language: Yup.string().required('Required!'),
    text: Yup.string().required("Required!")
  })

  const formik = useFormik({
    initialValues: initialValues,
    onSubmit: onSubmit,
    validate: validationSchema
  });

  return (
    <div>
      <form onSubmit={formik.handleSubmit}>
        <div className='form-control'>
          <label htmlFor='language'>Language</label>
          <input
            type='text'
            id='language'
            name='language'
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.language} />
          {(formik.touched.language && formik.errors.language) && <div className='form-error'>{formik.errors.language}</div>}
        </div>

        <div className='form-control'>
          <label htmlFor='text'>Text</label>
          <input
            type='text'
            id='text'
            name='text'
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.text} />
          {(formik.touched.text && formik.errors.text) && <div className='form-error'>{formik.errors.text}</div>}
        </div>

        {/* <input type='text' id='text' name='text'/> */}
        <button type='submit'>Submit</button>
      </form>
    </div>
  )
}

export default TextSubmissionForm;