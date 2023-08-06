## Introduction
This library assists CKAN editors with doing batch edits and pairs well with a library like pandas.

## Example usage

### Simple API commands

### Managed API commands
```python
with ckan_editor_utils.CKANEditorSession(ckan_url, ckan_key) as ckaneu:
    return ckaneu.delete_dataset(dataset_id).result
```
