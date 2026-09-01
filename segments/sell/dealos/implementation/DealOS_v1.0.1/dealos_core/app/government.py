def normalize_sam(item:dict):
    return {
      'source':'sam',
      'external_id':str(item.get('noticeId') or item.get('notice_id') or item.get('solicitationNumber') or ''),
      'title':item.get('title') or 'Untitled SAM opportunity',
      'url':item.get('uiLink') or item.get('additionalInfoLink'),
      'description':item.get('description'),
      'estimated_value_usd':None,
      'raw':item
    }
